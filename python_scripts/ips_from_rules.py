import argparse, textwrap, socket, struct
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
                    required=True,
                    help=textwrap.dedent('''\
                        look back number of days (default: %(default)s)
                        '''),
                    default="1"
                    )
parser.add_argument('--ruleid',
                    required=True,
                    help="Common rule id to investigate"
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
    matches = mongodb.MatchEvent.distinct("ip", {"_id": {"$gte": min_id}, "matches.id": int(args.ruleid)})
    return matches

if __name__ == '__main__':

    conf = conf()
    channels = getChannels(conf.mongo)
    acc = {}
    rule_matches = []
    
    # Loop through all channels in the DB
    for channel in channels:
        if "name" in channel:
            if "database" in channel:
                clients = getClients(conf.mongo, channel["database"]);
                for client in clients:
                    if args.customer and client != args.customer:
                        continue

                    client_db = client + "_data"
                    
                    # Setting up timeframe
                    now = datetime.datetime.now()
                    int_days = int(args.days)
                    start = now- datetime.timedelta(days=int_days)
                    min_id = ObjectId.from_datetime(start)

                    # Grabbing all matches from DB
                    matches = getMatches(conf.mongo, client_db, min_id)
                    matches = list(set(matches))
                    ips_file = open('ips.txt', 'wt')
                    
                    for item in matches:
                        ip = socket.inet_ntoa(struct.pack('!L', int(item)))
                        new_file = ips_file.write(ip + "\n")

                    ips_file.close()
                    print("Done")
