import argparse, textwrap
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
parser.add_argument('--command',
                    required=True,
                    help=textwrap.dedent('''\
                         action to perform:
                         list_customers\tprint all customer names
                         get_logs_events\tprint logs events for all customers
                         ''')
                   )
args = parser.parse_args()


def main():

    # create a new Client
    txapi = Client(args.url,args.api_key)

    # login to the api
    err = txapi.login()
    if err is not None:
        quit("Error: %s\ncould not obtain session_token!" % (err))

    # handle command = list_customers
    if (args.command == 'list_customers'):
        # get all customers
        list_customers, err = txapi.customers({'command':'list'})
        if err is not None:
            quit("Error: %s\ncould not list_customers!" % (err))
        # print customer names
        for customer in list_customers:
            print(customer['name'])

    # handle command = get_logs_events
    if (args.command == 'get_logs_events'):
        # get all customers
        list_customers, err = txapi.customers({'command':'list'})
        if err is not None:
            quit("Error: %s\ncould not list_customers!" % (err))
        # get logs events for each customer
        for customer in list_customers:
            logs, err = txapi.logs({
                                        'command':'events',
                                        'customer_name':customer['name']
                                    })
            if err is not None:
                quit("Error: %s\ncould not get logs events!" % (err))
            # print logs events for the customer
            print(logs)
        

if __name__ == '__main__':
    main()
