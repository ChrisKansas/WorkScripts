import argparse, textwrap
from aslookup import get_as_data
from tabulate import tabulate
from collections import Counter as counter

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
parser.add_argument('--list_type',
                    required=False,
                    help="list to target: blacklist, blocklist, whitelist"
                   )
parser.add_argument('--list_file',
                    required=False,
                    help="list of IPs to lookup"
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
    
    if args.list_type and args.list_file is None:
        # get existing list
        ip_list, err = txapi.lists({'command':"list_%s" % (args.list_type),'customer_name':args.customer})
        if err is not None:
            quit("Error: %s\ncould not get list!" % (err))
   
    elif args.list_file and args.list_type is None:
        with open(args.list_file, 'r') as data:
            ip_list = data.read().splitlines()
            ip_list = list(set(ip_list))

    else:
        quit("Error: Please provide either the list type or a new list of IPs!")

    # Create empty array for the ASNs
    asns = []
    
    # Loop through the list to look up the ASN for each IP
    for item in ip_list:
        asn = []
        if "/" in item:
            continue
        else:
            try:
                if args.list_type:
                    data = get_as_data(item['ip'], service='cymru')
                else:
                    data = get_as_data(item, service='cymru')

                asn.append(data[1])
                asn.append(data[6])
                asn.append(data[2])

                asns.append(asn)
            except:
                err = sys.exc_info()[0]
                print(err)
                print("Offending IP: %s" % item['ip'])
                continue

    # Create the table headers
    table = [['ASN', 'Country Code', 'ASN Name', 'Times Seen']]
    
    # Get the counts for the unique ASN data
    asns = [tuple(row) for row in asns]
    counted = counter(asns)
    counted = counted.items()

    updated_asns = []

    # Take count for each ASN item and append it; then add updated ASN to new list
    for item in counted:
        a = list(item[0])
        a.append(item[1])
        updated_asns.append(a)

    # Sort the ASNs from most seen to least
    updated_asns.sort(key=lambda x: int(x[3]),reverse=True)

    for asn in updated_asns:
        table.append(asn)
    
    # Open a text file to write the table of ASNs to it
    asn_file = open('%s_asns.txt' % args.customer, 'wt')
                    
    new_file = asn_file.write(tabulate(table) + "\n")

    asn_file.close()

    print("Finished Looking up ASNs - please see the %s_asns.txt file for results!" % args.customer)

if __name__ == '__main__':
    main()
