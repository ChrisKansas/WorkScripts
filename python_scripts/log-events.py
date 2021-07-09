#Tool for pulling audit events

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
parser.add_argument('--event_type',
                    required=True,
                    help="event type to pull - block_events, match_events, audit_events"
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

    # get audit events
    audit_events, err = txapi.logs_v2({'command': args.event_type,'customer_name': args.customer, 'time_start': "2021-03-23T08:00:57+00:00", "hostname": "api.naea1.uds.lenovo.com", "limit": 1000})

    for event in audit_events['data']:
        print(event)
    
if __name__ == '__main__':
    main()
