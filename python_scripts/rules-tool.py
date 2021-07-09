import argparse, textwrap, json, hashlib

import sys
sys.path.append('../py-api-client/client')
from client import Client


# get arguments
parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument('--api_key',
                    required=True,
                    help="threatx provisioning API key"
                   )
parser.add_argument('--url',
                    required=False,
                    help=textwrap.dedent('''\
                        threatx provisioning API url
                        (default: %(default)s)
                        '''),
                    default="https://provision.threatx.io/tx_api/v1/"
                   )
parser.add_argument('--customer',
                    required=True,
                    help="customer name to target"
                   )
parser.add_argument('--action',
                    required=True,
                    help="desired action for tool: pull, update"
                   )
parser.add_argument('--rule_type',
                    required=True,
                    help="ruleset to target: customer, profiler, whitelist, common"
                   )
parser.add_argument('--rules_file',
                    required=False,
                    help="local rules.json file to apply to the target ruleset/customer"
                   )
parser.add_argument('--output',
                    required=False,
                    help="what do you wanna name the json output file; just the name, no extension needed"
                   )
parser.add_argument('--commit',
                    required=False,
                    help="commit ruleset changes to API",
                    action='store_true',
                    default=False
                   )
args = parser.parse_args()


def upsert_rule(txapi,ruleset_existing,new):
    # update a rule
    for existing in ruleset_existing:
        # match against existing rules
        if new['id'] == existing['id']:
            # check if the rule needs updating
            hash_new = hashlib.sha224(json.dumps(new).encode('utf-8')).hexdigest()
            hash_existing = hashlib.sha224(json.dumps(existing).encode('utf-8')).hexdigest()
            if hash_new != hash_existing:
                # either update the rule or threaten to
                if args.commit:
                    return txapi.rules({'command':'update_%s_rule' % (args.rule_type),'customer_name':args.customer,'id':new['id'],'rule':new})
                else:
                    _, err = txapi.rules({'command':'validate_rule','customer_name':args.customer,'rule':new})
                    return ("Rule with id: %s will be updated." % (new['id']), err)
            # do nothing
            return ('Rule with id: %s has no changes.' % (new['id']), None)
    # either insert the rule or threaten to
    if args.commit:
        return txapi.rules({'command':'new_%s_rule' % (args.rule_type),'customer_name':args.customer,'rule':new})
    else:
        _, err = txapi.rules({'command':'validate_rule','customer_name':args.customer,'rule':new})
        return ("Rule with id: %s will be inserted." % (new['id']), err)

def main():

    # create a new Client
    txapi = Client(args.url,args.api_key)

    # login to the api
    err = txapi.login()
    if err is not None:
        quit("Error: %s\ncould not obtain session_token!" % (err))

    # confirm we have access to this customer
    _, err = txapi.customers({'command':'get','name':args.customer})
    if err is not None:
        quit("Error: %s\ncould not get customer!" % (err))

    # get existing ruleset
    ruleset_existing, err = txapi.rules({'command':'list_%s_rules' % (args.rule_type),'customer_name':args.customer})
    if err is not None:
        quit("Error: %s\ncould not get rules!" % (err))

    if args.action == "pull":
        if args.output:
            with open('%s.json' % (args.output), 'w+') as outfile:
                json.dump(ruleset_existing, outfile, indent=2)
        else:
            quit("Please use '--output' to provide the output file name.")

    elif args.action == "update":
        # load the new ruleset
        if args.rules_file:
            with open(args.rules_file, 'r') as data:
                ruleset_new = json.load(data)
        else:
            quit("Please use '--rules_file' to provide the updated rule file.")

        # delete any rules not in new ruleset
        for existing in ruleset_existing:
           if existing['id'] not in [rule['id'] for rule in ruleset_new]:
              # either delete the rule or threaten to
              if args.commit:
                  message, err = txapi.rules({'command':'delete_%s_rule' % (args.rule_type),'customer_name':args.customer,'id':existing['id']})
                  if err is not None:
                      quit("Error: %s\ncould not delete rule %s" % (err,existing['id']))
                  print(message)
              else:
                  print("Rule with id %s will be deleted." % (existing['id']))

        # upsert from new ruleset
        for new in ruleset_new:
            message, err = upsert_rule(txapi,ruleset_existing,new)
            if err is not None:
                quit("Error: %s\ncould not upsert rule %s" % (err,new['id']))
            print(message)

    else:
        quit("Please provide a valid action!")

if __name__ == '__main__':
    main()
