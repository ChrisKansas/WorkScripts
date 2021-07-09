#Tool for deleting customers/tenants

import argparse, textwrap, sys, json
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
parser.add_argument('--action',
                    required=True,
                    help="action to be performed by the tool: list, get, add, update, delete"
                   )
parser.add_argument('--channel',
                    required=False,
                    help="channel name for tenant to be added to"
                   )
parser.add_argument('--tenant_name',
                    required=False,
                    help="tenant name for getting or adding a tenant"
                   )
parser.add_argument('--contact_email',
                    required=False,
                    help="contact email for tenant"
                   )
parser.add_argument('--sso_enabled',
                    required=False,
                    help="true/false - is SSO enabled"
                   )
parser.add_argument('--saml_metadata_url',
                    required=False,
                    help="saml URL"
                   )
parser.add_argument('--customer_file',
                    required=False,
                    help="file of customers to delete"
                   )
parser.add_argument('--commit',
                    required=False,
                    help="commit tenant changes to API",
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
    
    # get customers
    if args.action == "list" or args.action == "get" or args.action == "update":
        customers_existing, err = txapi.customers({'command':'list_all'})
        if err is not None:
            quit("Error: %s\ncould not get tenants!" % (err))
    
    # List out all Tenants for all Channels
    if args.action == "list":
        with open('all_customers.json', 'w+') as outfile:
            json.dump(customers_existing, outfile, indent=2)
    
    # Get a Specific Tenant        
    elif args.action == "get":
        if args.tenant_name:
            for customer in customers_existing:
                if args.tenant_name == customer["name"]:
                    print("----------%s----------\n" % (args.tenant_name.upper()))
                    pretty_customer = json.dumps(customer, indent=2)
                    print(pretty_customer + "\n")
        else:
            print("Error: Please provide the tenant name!")
    
    # Tenant Addition
    elif args.action == "add":
        tenant = {}
        if args.tenant_name:
            tenant['name'] = args.tenant_name
            if args.channel:
                tenant['channel'] = args.channel
                if args.contact_email:
                    tenant['contact_email'] = args.contact_email
                    tenant['active'] = True
                    tenant['description'] = args.tenant_name
                    tenant['autoblock_timeout'] = 1800
                    tenant['autoblock_threshold'] = 70
                    tenant['block_embargo'] = False
                    tenant['notify_threshold'] = 70
                    tenant['tenant_admin_default'] = True
                    if args.commit:
                        new_tenant, err = txapi.customers({'command': 'new', 'customer': tenant})
                        if err is not None:
                            quit("Error: %s\n could not add new tenant!" % (err))
                        print(new_tenant)
                    else:
                        print("%s will be added!" % args.tenant_name)
                else:
                    quit("Error: Please provide a contact email for the new tenant!")
            else:
                quit("Error: Please provide the channel to which this tenant will be added!")
        else:
            quit("Error: Please provide the name of the new tenant!")

    # Tenant Updating
    elif args.action == "update":
        if args.tenant_name:
            for customer in customers_existing:
                if args.tenant_name == customer["name"]:
                    tenant = {}
                    tenant = customer
                    if args.contact_email:
                        tenant["contact_email"] = args.contact_email
                    if args.sso_enabled:
                        if args.saml_metadata_url:
                            tenant["sso"]["enabled"] = True
                            tenant["sso"]["required"] = False
                            tenant["sso"]["saml_metadata_url"] = args.saml_metadata_url
                        else:
                            quit("Error: Please provide the SAML metadata URL!")
                    if args.commit:
                        updated_tenant, err = txapi.customers({'command': 'update', 'name': args.tenant_name, 'customer': tenant})
                        if err is not None:
                            quit("Error: %s\n could not update the tenant!" % (err))
                        print(updated_tenant)
                    else:
                        quit("%s will be updated!" % args.tenant_name)
        else:
            quit("Error: Please provide a tenant name!")

    # Tenant Deletion
    elif args.action == "delete":

        # Check if customer file provided
        if args.customer_file:
            
            # Read out data from file
            try:
                with open(args.customer_file, 'r') as data:
                    customer_file = data.read().splitlines()
            except:
                quit("Error: Please provide a valid text file!")
            
            # Loop through each line/customer
            for customer in customer_file:

                # confirm we have access to each customer
                _, err = txapi.customers({'command':'get','name':customer})
                if err is not None:
                    quit("Error: %s\ncould not get customer!" % (err))
                
                # Check if commit is set
                if args.commit:
                    deleted_customer, err = txapi.customers({'command':'delete','name':customer})
                    if err is not None:
                        quit("Error: %s\ncould not delete tenant!" % (err))
                    else:
                        print(deleted_customer)

                # If not; confirm the customers that will be deleted
                else:
                    print("%s will be deleted!" % customer)
        else:
            quit("Error: Please use '--customer_file' to provide a file with tenant names to be deleted!")
    
    # Invalid Action Provided
    else:
        quit("Error: Please provide a valid action!")
    
if __name__ == '__main__':
    main()
