import argparse, textwrap, json
from config import Config as conf
import datetime
from bson.objectid import ObjectId

# get arguments
parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument('--customer',
                    required=False,
                    help="restrict scrope to a particular customer"
                   )
parser.add_argument('--days',
                    required=False,
                    help=textwrap.dedent('''\
                        look back number of days (default: %(default)s)
                        '''),
                    default="1"
                    )
parser.add_argument('--ruleid',
                    required=False,
                    help="Common rule id to investigate"
                   )
parser.add_argument('--output',
                    required=False,
                    help="output match events to specified file; only name required, will output as .json"
                   )
parser.add_argument('--ignore-customers',
                    required=False,
                    help="restrict scrope to a particular customer"
                   )

args = parser.parse_args() 

def getChannels(client):
    mongodb = client["customer"]
    channels = mongodb.channeldb.find()
    return channels

def getClients(client, db):
    mongodb = client[db];
    clients = mongodb.clients.distinct("name")
    return clients

def getMatches(client, db, min_id):
    mongodb = client[db];
    if args.ruleid:
        matches = mongodb.MatchEvent.distinct("ip", {"matches.id": int(args.ruleid)})
    else:
        matches = mongodb.MatchEvent.find({"_id": {"$gte": min_id}, "matches.beta": True})
    return matches

def processMatches(acc, matches):
    for match in matches:
        if "matches" in match:
            match.pop('_id')
            match.pop('received')
            rule_matches.append(match)
            for rule in match["matches"]:
                if ("beta" in rule and rule["beta"] == True) or args.ruleid:
                    if ("id" in rule and not args.ruleid) or (args.ruleid and rule['id'] == int(args.ruleid)):
                        id = rule["id"]
                        if id in acc:
                            acc[id] += 1
                        else:
                            acc[id] = 1

if __name__ == '__main__':

    conf = conf()
    channels = getChannels(conf.mongo)
    acc = {}
    rule_matches = []
    ignore_customers = []
    
    # Which customers need to be ignored
    if args.ignore_customers:
        ignore_customers = args.ignore_customers.split(",")
    
    # Loop through all channels in the DB
    for channel in channels:
        if "name" in channel:
            if "database" in channel:
                clients = getClients(conf.mongo, channel["database"]);
                for client in clients:
                    if args.customer and client != args.customer:
                        continue

                    if client in ignore_customers:
                        continue
                    
                    client_db = client + "_data"
                    
                    # Setting up timeframe
                    now = datetime.datetime.now()
                    int_days = int(args.days)
                    start = now- datetime.timedelta(days=int_days)
                    min_id = ObjectId.from_datetime(start)

                    # Grabbing all matches from DB
                    matches = getMatches(conf.mongo, client_db, min_id)

                    # Appends matches for output; provides match numbers for beta or specified rule IDs
                    #processMatches(acc, matches)
    
    print(set(matches))
    
    # Format the output for readable JSON
    if args.output:
        with open('%s.json' % (args.output), 'w+') as outfile:
            json.dump(rule_matches, outfile, indent=2)
    
    # Print out the number of matches
    #print("Rule matches: {}".format(acc))
