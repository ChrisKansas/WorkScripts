#Tool for handling entities - providing entity links or resetting entities

import argparse, textwrap, sys
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
                    help="link, reset - determines the tool's action"
                   )
parser.add_argument('--ip_list',
                    required=True,
                    help="list file of IPs for entity IDs to reset"
                   )
parser.add_argument('--commit',
                    required=False,
                    help="commit entity reset changes to API",
                    action='store_true',
                    default=False
                   )
args = parser.parse_args()

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
    
    # take IP list and convert to list
    try:
        with open(args.ip_list, 'r') as data:
                ips = data.read().splitlines()
    except:
        quit("Please provide a valid list!")

    # list the entity links
    if args.action == "link":
        
        # get entities
        entities, err = txapi.entities({'command':'list', 'customer_name':args.customer, 'query': {'ip_addresses': ips}})
        if err is not None:
            quit("Error: %s\ncould not get entities!" % (err))

        # print entity links for IPs
        for entity in entities:
            print("%s: https://x.threatx.io/customers/%s/entities/%s; State: %s" % (entity["actors"][0]["ip_addr"], args.customer, entity["actors"][0]["id"], entity["actors"][0]["state"]))

    # reset the entity list
    elif args.action == "reset":
        
        # Commit to all the API calls
        if args.commit:

            entity_ids = []
            
            # Check if the number of IPs is greater than 1k due to list limitation
            if len(ips) > 1000:
                ip_list = []
                innerlist = []

                # Move IPs into 1k list chunks
                for index, ip in enumerate(ips):
                    innerlist.append(ip.strip())
                    if (index + 1) % 1000 == 0:
                        ip_list.append(innerlist)
                        innerlist = []
                    elif (index + 1) == len(ips):
                        ip_list.append(innerlist)

                # get entities
                for item in ip_list:
                    entities, err = txapi.entities({'command':'list', 'customer_name':args.customer, 'query': {'ip_addresses': item}})
                    if err is not None:
                        quit("Error: %s\ncould not get entities!" % (err))
                    for entity in entities:
                        entity_ids.append(entity['id'])
            
            else:
                entities, err = txapi.entities({'command':'list', 'customer_name':args.customer, 'query': {'ip_addresses': ips}})
                if err is not None:
                    quit("Error: %s\ncould not get entitites!" % (err))
                for entity in entities:
                    entity_ids.append(entity['id'])

            # reset entities
            for entity_id in entity_ids:
                reset_response, err = txapi.entities({'command': 'reset', 'customer_name': args.customer, 'id': entity_id})
                if err is not None:
                    quit("Error: %s\ncould not reset entity!" % err)
                else:
                    print("Entity: %s has been reset." % entity_id)
        
        # Dry Run Mode
        else:
            print("%s - Entities will be reset!!" % (args.customer.capitalize()))
    
    else:
        quit("Error: Please provide a valid action!")
    
if __name__ == '__main__':
    main()
