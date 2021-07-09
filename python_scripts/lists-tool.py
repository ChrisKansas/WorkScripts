import argparse, textwrap, json, hashlib, time, ipaddress

import sys
sys.path.append('../py-api-client/client')
from client import Client
from functools import cmp_to_key

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
parser.add_argument('--description',
                    required=False,
                    help=textwrap.dedent('''\
                        Custom description to apply to ALL entries.
                        (default: %(default)s)
                        '''),
                    default="Added by ThreatX SOC"
                   )
parser.add_argument('--customer',
                    required=True,
                    help="customer name to target"
                   )
parser.add_argument('--list_type',
                    required=True,
                    help="list to target: blacklist, blocklist, whitelist"
                   )
parser.add_argument('--action',
                    required=True,
                    help="action to perform: add, remove, clear, bulk_add, sync_list, flip, list, print_sorted_list"
                   )
parser.add_argument('--list_file',
                    required=False,
                    help="local newline-separated file to apply to the target customer"
                   )
parser.add_argument('--customer_sync_from',
                    required=False,
                    help="the customer whose list you want to add to another customer"
                   )
parser.add_argument('--flip_to',
                    required=False,
                    help="list type to flip IPs to; IPs come from '--list_type'"
                   )
parser.add_argument('--commit',
                    required=False,
                    help="commit list changes to API",
                    action='store_true',
                    default=False
                   )
args = parser.parse_args()

# Compare Function
def customComparator(a, b):

    # Breaking into the octets
    octetsA = [int(x) for x in a.strip().replace('/', '.').split(".")]
    octetsB = [int(x) for x in b.strip().replace('/', '.').split(".")]

    if octetsA == octetsB:
        return 0
    elif octetsA[0] > octetsB[0]:
        return 1
    elif octetsA[0] < octetsB[0]:
        return -1
    elif octetsA[1] > octetsB[1]:
        return 1
    elif octetsA[1] < octetsB[1]:
        return -1
    elif octetsA[2] > octetsB[2]:
        return 1
    elif octetsA[2] < octetsB[2]:
        return -1
    elif octetsA[3] > octetsB[3]:
        return 1
    elif octetsA[3] < octetsB[3]:
        return -1

# Function to sort the IP Addresses
def sortIPAddress(arr):

    arr = sorted(arr, key = cmp_to_key(customComparator))

    return arr

# Recursive Binary Search
def binary_search(arr, low, high, x):

    # Check base case
    if high >= low:
        mid = (high + low) // 2
        if arr[mid] == x:
            return arr[mid]
        elif ipaddress.IPv4Address(arr[mid].split('/')[0]) > ipaddress.IPv4Address(x):
            return binary_search(arr, low, mid - 1, x)
        else:
            return binary_search(arr, mid + 1, high, x)
    else:
        return -1

# add contents of a file to an existing list
def list_add(txapi,customer,list_type,existing_ips,list_file):

    def lineparse(item):
        linearr = item.strip().split(' ',1)
        ip = linearr[0]
        if len(linearr) == 1:
            desc = args.description
        else:
            desc = str(linearr[1].strip())
        return ip, desc

    if args.commit:

        # Start timer on sync function
        start_time = time.time()

        for item in list_file:

            # Check as time gets closer to 20 minutes; login again
            if time.time() - start_time >= 1200:
                err = txapi.login()
                if err is not None:
                    quit("Error: %s\ncould not obtain session_token!" % (err))

            ip, desc = lineparse(item)

            if ip in existing_ips:
                continue
            else:
                resp, err = txapi.lists({'command':"new_%s" % (list_type),'customer_name': customer,'entry':{
                    'ip': ip,
                    'description': desc,
                    'created': int(time.time())
                    }})
                if err is not None:
                    quit("Error: %s" % (err))
                else:
                    print(resp)
    else:
        for item in list_file:
            ip, desc = lineparse(item)
            print("%s entry for IP %s will be added (%s)" % (list_type,ip,desc))

    return None

# use bulk add to update existing  list
def bulk_add(txapi,customer,list_type,list_file,*ips):

    # Check for additional args
    if len(ips) >= 1:
        existing_ips = ips[0]
    else:
        existing_ips = ""
    
    # Parse the list line
    def lineparse(item):
        if "," in item:
            linearr = item.strip().split(',')
            ip = linearr[0]
            if len(linearr) > 1:
                add_desc = linearr[1]
            if len(linearr) >= 2 and args.description:
                desc = add_desc + args.description
            else:
                desc = str(linearr[1].strip())
        else:
            ip = item.strip()
            desc = args.description

        return ip, desc

    if args.commit:
        total_list = []
        total_ips = 0

        # Start timer on sync function
        start_time = time.time()

        # Loop through the list
        for item in list_file:

            # Check as time gets closer to 20 minutes; login again
            if time.time() - start_time >= 1200:
                err = txapi.login()
                if err is not None:
                    quit("Error: %s\ncould not obtain session_token!" % (err))
                
                # Reset timer
                start_time = time.time()

            ip, desc = lineparse(item)

            # If checking an existing list - remove duplicates
            if existing_ips != "" and ip in existing_ips:
                continue
            else:
                total_list.append({"ip": ip, "description": desc, "created": 1})

                # Bulk command has limit of 1k IPs; reduced to 500 for API timeouts
                if len(total_list) == 500:
                    bulk_update, err = txapi.lists({'command': 'bulk_new_%s' % (list_type), 'customer_name': customer, "items": total_list})
                    
                    if err is not None:
                        pretty_error = json.dumps(err, indent=2)
                        print(pretty_error)
                        print("Error: Failed to add IPs - see above.")
                    else:
                        total_ips += 500
                        print("500 IPs have been added to the %s!" % list_type)
                    total_list = []
                else:
                    continue
        
        # Get total amount of IPs to be added
        total_ips += len(total_list)

        # Run command one last time for the last <500 IPs on the list
        bulk_update, err = txapi.lists({'command': 'bulk_new_%s' % (list_type), 'customer_name': customer, "items": total_list})
        
        if err is not None:
            # Made errors more readable
            pretty_error = json.dumps(err, indent=2)
            print(pretty_error)
            print("Error: Failed to add IPs - see above.")
        else:
            print("Total number of IPs added to the %s: %s" % (list_type, total_ips))

    else:
        for item in list_file:
            ip, desc = lineparse(item)
            print("%s entry for IP %s will be added (%s)" % (list_type,ip,desc))

    return None

def bulk_remove(txapi,customer,list_type,list_file):

    def lineparse(item):
        if "," in item:
            linearr = item.strip().split(',')
            ip = linearr[0]
            if len(linearr) > 1:
                add_desc = linearr[1]
            if len(linearr) >= 2 and args.description:
                desc = add_desc + args.description
            else:
                desc = str(linearr[1].strip())
        else:
            ip = item
            desc = args.description

        return ip, desc

    if args.commit:
        
        total_list = []
        total_ips = 0

        for item in list_file:
            ip, desc = lineparse(item)
            
            total_list.append({"ip": ip, "description": desc, "created": 1})

            # Bulk command has limit of 1k IPs
            if len(total_list) == 1000:
                bulk_delete, err = txapi.lists({'command': 'bulk_delete_%s' % (list_type), 'customer_name': customer, "items": total_list})
                
                if err is not None:
                    quit("Error: %s\n could not bulk remove!" % (err))
                else:
                    total_ips += 1000
                    print("1k IPs have been removed from the %s!" % list_type)
                total_list = []
            else:
                continue

        total_ips += len(total_list)

        # Run command one last time for the last <1k IPs on the list
        bulk_delete, err = txapi.lists({'command': 'bulk_delete_%s' % (list_type), 'customer_name': customer, "items": total_list})
        
        if err is not None:
            quit("Error: %s\n could not bulk remove!" % (err))
        else:
            print("Total number of IPs removed from the %s: %s" % (list_type, total_ips))

    else:
        for item in list_file:
            ip, desc = lineparse(item)
            print("%s entry for IP %s will be removed (%s)" % (list_type,ip,desc))

    return None

# remove contents of the existing list where they exist in file
def list_remove(txapi,customer,list_type,list_existing,list_file):

    if args.commit:
        for item in list_existing:
            if item['ip'] in list_file:
                resp, err = txapi.lists({'command':"delete_%s" % (list_type),'customer_name': customer,
                    'ip':item['ip']
                })
                if err is not None:
                    quit("Error: %s" % (err))
                else:
                    print(resp)
    else:
        for item in list_existing:
            if item['ip'] in list_file:
                print("%s entry for IP %s will be removed (%s)" % (list_type,item['ip'],item['description']))

    return None

# clear all existing contents from the list
def list_clear(txapi,customer,list_type,list_existing):

    if args.commit:
        for item in list_existing:
            resp, err = txapi.lists({'command':"delete_%s" % (list_type),'customer_name': customer,
                'ip':item['ip']
            })
            if err is not None:
                quit("Error: %s" % (err))
            else:
                print(resp)
    else:
        for item in list_existing:
            print("%s entry for IP %s will be removed (%s)" % (list_type,item['ip'],item['description']))

    return None

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

    # get existing list
    list_existing, err = txapi.lists({'command':"list_%s" % (args.list_type),'customer_name':args.customer})
    if err is not None:
        quit("Error: %s\ncould not get list!" % (err))

    # 'clear' doesn't need a list_file argument
    if args.action == 'clear':
        list_clear(txapi,args.customer,args.list_type,list_existing)

    # 'add', 'remove', 'bulk_add' need a list_file argument
    if args.list_file is not None:
        # load the list_file
        with open(args.list_file, 'r') as data:
            list_file = data.read().splitlines()
            list_file = list(set(list_file))

        if args.action == 'add':
            list_add(txapi,args.customer,args.list_type,list_existing,list_file)
        elif args.action == 'remove':
            list_remove(txapi,args.customer,args.list_type,list_existing,list_file)
        elif args.action == 'bulk_add':
            existing_ips = []
            for item in list_existing:
                existing_ips.append(item['ip'])
            bulk_add(txapi,args.customer,args.list_type,list_file,existing_ips)
        else:
            quit('Error: invalid action command')

    # 'sync_list' does not need a list_file argument
    elif args.action == 'sync_list':
        # Grab List for 'from' Customer
        list_to_sync_from, err = txapi.lists({'command':"list_%s" % (args.list_type),'customer_name':args.customer_sync_from})
        if err is not None:
            quit("Error: %s\n Could not get %s's list!" % (err,args.customer_sync_from))

        # Create lists
        customer_to_sync = []
        customer_sync_from = []
        new_ips = []
        
        # Pull IPs for targeted customer
        for item in list_existing:
            customer_to_sync.append(item['ip'])

        # Pull IPs for customer to sync from
        for item in list_to_sync_from:
            customer_sync_from.append(item['ip'])
        
        # Sort the IP lists
        customer_to_ips = sortIPAddress(customer_to_sync)
        customer_from_ips = sortIPAddress(customer_sync_from)

        # Check for IPs not in targeted customer's list
        for item in customer_from_ips:
            
            # Create junk var for CIDR range 
            junk = ""
            if "/" in item:
                item, junk = item.split('/')

            # Search for duplicates
            exist = binary_search(customer_to_ips, 0, len(customer_to_ips)-1, item)
            
            # If dupe not found; add to list; put CIDR range back together
            if exist == -1:
                if junk != "":
                    item = item + "/" + junk
                    new_ips.append(item)
                else:
                    new_ips.append(item)
                continue
            else:
                continue

        print("Number of IPs to add: %s" % len(new_ips))

        # Update targeted customer's list with new IPs
        bulk_add(txapi,args.customer,args.list_type,new_ips)

    elif args.action == "flip":
        new_ips = []
        for item in list_existing:
            new_ips.append(item['ip'])

        bulk_remove(txapi,args.customer,args.list_type,new_ips)
        bulk_add(txapi,args.customer,args.flip_to,new_ips)

    elif args.action == "list":
        print("Total number of IPs on %s's %s: %s" % (args.customer, args.list_type, len(list_existing)))

    elif args.action == "print_sorted_list":

        # Create list
        customer_list = []
        
        # Pull IPs for targeted customer
        for item in list_existing:
            customer_list.append(item['ip'])

        # Sort the IP lists
        customer_ips = sortIPAddress(customer_list)

        ips_file = open('%s_%s_ips.txt' % (args.customer, args.list_type), 'wt')

        for ip in customer_ips:
            new_file = ips_file.write(ip + "\n")

        ips_file.close()
        print("Sorted list retrieved - please see new file: %s_%s_ips.txt" % (args.customer, args.list_type))

    else:
        quit('Error: Please provide the list of IPs!')

if __name__ == '__main__':
    main()
