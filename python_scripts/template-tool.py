# Tool for updating custom templates via the API

import argparse, textwrap, sys, difflib, os
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
                    help="action for the tool - pull, update"
                   )
parser.add_argument('--updated_template',
                    required=False,
                    help="the updated customer template file"
                   )
parser.add_argument('--commit',
                    required=False,
                    help="commit template changes to API",
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
   
    # get prod template
    existing_template, err = txapi.templates({'command':'get', 'customer_name': args.customer})
    if err is not None:
        quit("Error: %s\ncould not get rules!" % (err))
    
    # Pulling/printing existing prod template
    if args.action == "pull":
        print(existing_template["template"])

    # Updating existing prod template
    elif args.action == "update":
    
        # write current prod template to file
        file = open('old_template', 'w')
        file.write(existing_template["template"] + "\n")
        file.close()
       
        # take current prod template file and read into var for checking differences
        with open('old_template', 'r') as data:
            old_template = data.read().splitlines()
        
        # remove prod template file
        os.remove('old_template')

        if args.updated_template:
            # take updated template file and read into var for checking differences
            with open(args.updated_template, 'r') as data:
                updated_template = data.read().splitlines()

            # updated template file to push for changes
            with open(args.updated_template, 'r') as data:
                template_file = data.read()
        
            #Check if there are differences
            if next(difflib.context_diff(old_template, updated_template, fromfile='%s - Current Prod Template' % (args.customer), tofile='%s - New Updated Template' % (args.customer), n=0), -1) == -1:
                quit("\nThere are no differences between prod and github!\n")
            else:
                # print differences between prod template and updated template
                print("\n##########BELOW ARE THE CURRENT DIFFERENCES BETWEEN PROD AND THE UPDATED TEMPLATE##########\n")
                
                for line in difflib.context_diff(old_template, updated_template, fromfile='%s - Current Prod Template' % (args.customer), tofile='%s - New Updated Template' % (args.customer), n=0):
                    print(line)

            print("\n")

            #Commit changes to API
            if args.commit:
                response, err = txapi.templates({'command':'set', 'customer_name': args.customer, 'template': template_file})
                if err is not None:
                    quit("Error: %s\ncould not update template!" % (err))
                else:
                    print(response)
            else:
                print("%s template will be updated!\n" % (args.customer))

        else:
            sys.exit("Error: Please use '--updated_template' to provide the updated template!")

    else:
        sys.exit("Error: Please provide a valid action!")

if __name__ == '__main__':
    main()
