#SOC Tool for Handling Sites via the API

import argparse, textwrap, json, csv

import sys
sys.path.append("../py-api-client/client")
from client import Client

# get arguments
parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument("--api_key",
                    required=True,
                    help="threatx provisioning API key"
                   )
parser.add_argument("--url",
                    required=False,
                    help=textwrap.dedent("""\
                        threatx provisioning API url
                        (default: %(default)s)
                        """),
                    default="https://provision.threatx.io/tx_api/v1/"
                   )
parser.add_argument("--customer",
                    required=True,
                    help="customer name to target"
                   )
parser.add_argument("--action",
                    required=True,
                    help="action for sites - list, new, get, delete, update, bulk_add, bulk_update, bulk_delete"
                   )
parser.add_argument("--site_name",
                    required=False,
                    help="For GET, NEW, UPDATE actions - provide site name"
                   )
parser.add_argument("--backend",
                    required=False,
                    help="Provide the backend info for the site"
                   )
parser.add_argument("--blocking",
                    required=False,
                    help="Is blocking enabled? true/false"
                   )
parser.add_argument("--blocking_types",
                    required=False,
                    help="Which types are being enabled? manual, risk, and/or request"
                   )
parser.add_argument("--ssl",
                    required=False,
                    help="Is ssl enabled? true/false"
                   )
parser.add_argument("--http2",
                    required=False,
                    help="Is http2 enabled? true/false"
                   )
parser.add_argument("--ssl_redirect",
                    required=False,
                    help="Is ssl_redirect enabled? true/false"
                   )
parser.add_argument("--cert",
                    required=False,
                    help="Provide the cert chain file."
                   )
parser.add_argument("--ssl_protocols",
                    required=False,
                    help="Please provide the protocol(s) you would like set for the site"
                   )
parser.add_argument("--ssl_ciphers",
                    required=False,
                    help="Please provide a list of ciphers you would like set for the site."
                   )
parser.add_argument("--bulk_file",
                    required=False,
                    help="CSV File of sites to add - include name, backend, blocking [if needed], ssl_blob. Regular file with each site name for updating or deleting sites."
                   )
parser.add_argument('--commit',
                    required=False,
                    help="commit site changes to API",
                    action='store_true',
                    default=False
                   )
args = parser.parse_args()

def site_delete(txapi, customer, site):
    deleted_site, err = txapi.sites({"command": "delete", "customer_name": customer, "name": site})
    if err is not None:
        quit("Error: %s\n could not delete site!" % (err))
    return deleted_site

def print_output(output_type, *args):
    if args:
        ad_arg = args
        if output_type == "site_name":
            print("\n---------------%s---------------\n" % ad_arg[0]["hostname"])
            print(ad_arg)
        elif output_type == "site_error":
            print("Error: %s is not a configured site!" % ad_arg[0])
        elif output_type == "bulk_file_error":
            sys.exit("Error: Please provide a list of sites to be %s!" % ad_arg[0])
        elif output_type == "dry_run":
            print("%s will be %s!" % (ad_arg[0], ad_arg[1]))
    else:
        if output_type == "site_name_error":
            sys.exit("Error: Please provide a site name!")
        elif output_type == "cert_error":
            sys.exit("Error: Please provide the certificate chain!")
        elif output_type == "blocking_type_error":
            sys.exit("Error: Please provide the blocking types to enable!")
        elif output_type == "ssl_error":
            sys.exit("Error: Please provide true or false for SSL!")
        elif output_type == "ssl_true_error":
            sys.exit("Error: Please set ssl to true!")
        elif output_type == "backend_error":
            sys.exit("Error: Please provide the site backend info!")
        elif output_type == "action_error":
            sys.exit("Error: Please provide a valid action type!")

def main():

    # create a new Client
    txapi = Client(args.url,args.api_key)

    # login to the api
    err = txapi.login()
    if err is not None:
        quit("Error: %s\ncould not obtain session_token!" % (err))
    
    # confirm we have access to this customer
    _, err = txapi.customers({"command":"get","name":args.customer})
    if err is not None:
        quit("Error: %s\ncould not get customer!" % (err))
    
    # get existing sites
    if args.action in ["list", "get", "update", "bulk_update", "delete", "bulk_delete"]:
        existing_sites, err = txapi.sites({"command":"list","customer_name":args.customer})
        if err is not None:
            quit("Error: %s\ncould not get sites!" % (err))
    
    # Set Block Types
    manual = False
    risk = False
    request = False

    # list sites
    if args.action == "list":
        for site in existing_sites:
            print_output("site_name", site)
        print("\n")
    
    # get specific site
    elif args.action == "get":
        if args.site_name:
            for site in existing_sites:
                if site["hostname"] == args.site_name:
                    return print_output("site_name", site)
            print_output("site_error", args.site_name)
        else:
            print_output("site_name_error")

    # Add new site
    elif args.action == "new":
        payload = {}
        payload["command"] = args.action
        payload["customer_name"] = args.customer
        payload["site"] = {}
        payload["site"]["isEnabled"] = True
        
        if args.site_name:
            payload["site"]["hostname"] = args.site_name
            
            if args.backend:
                payload["site"]["backend"] = [[args.backend, True]]
                
                if args.blocking and args.blocking.lower() == "true":
                    if args.blocking_types:
                        site_blocking_types = args.blocking_types.replace(" ", "").split(",")
                        for block_type in site_blocking_types:
                            if block_type.lower() == "manual":
                                manual = True
                            elif block_type.lower() == "risk":
                                risk = True
                            elif block_type.lower() == "request":
                                request = True
                    else:
                        print_output("blocking_type_error")
                    
                payload["site"]["risk_based_blocking"] = risk
                payload["site"]["request_blocking"] = request
                payload["site"]["manual_action_blocking"] = manual
                
                if args.ssl:
                    if args.ssl.lower() == "true":
                        if args.cert:
                            with open(args.cert) as cert_file:
                                cert = cert_file.read()
                                payload["site"]["ssl_enabled"] = True
                                payload["site"]["ssl_blob"] = cert
                        else:
                            print_output("cert_error")
                
                if args.http2:
                    payload["site"]["http2_enabled"] = True
                if args.ssl_redirect:
                    payload["site"]["ssl_redirect"] = True
                
                if args.commit:
                    new_site, err = txapi.sites(payload)
                    if err is not None:
                        quit("Error: %s\n could not add site!" % (err))
                    print(new_site)
                else:
                    print_output("dry_run", args.site_name, "added")
            else:
                print_output("backend_error")
        else:
            print_output("site_name_error")
    
    # Delete a site
    elif args.action == "delete":
        if args.site_name:
            for site in existing_sites:
                if site["hostname"] == args.site_name:
                    if args.commit:
                        deleted_site = site_delete(txapi, args.customer, args.site_name)
                        return print(deleted_site)
                    else:
                        return print_output("dry_run", args.site_name, "deleted")
            print_output("site_error", args.site_name)
        else:
            print_output("site_name_error")

    # Bulk Site Delete
    elif args.action == "bulk_delete":
        if args.bulk_file:
            with open(args.bulk_file, 'r') as data:
                bulk_file = data.read().splitlines()
            for site in bulk_file:
                for i, existing_site in enumerate(existing_sites):
                    if existing_site["hostname"] == site.strip():
                        if args.commit:
                            deleted_site = site_delete(txapi, args.customer, site.strip())
                            print(deleted_site)
                            break
                        else:
                            print_output("dry_run", site, "deleted")
                            break
                    elif existing_site["hostname"] != site.strip() and i == len(existing_sites) - 1:
                        print_output("site_error", site.strip())
                        break
        else:
            print_output("bulk_file_error", "deleted")

    # Update a site
    elif args.action == "update":
        payload = {}
        payload["command"] = args.action
        payload["customer_name"] = args.customer
        payload["name"] = args.site_name
        current_site = {}
        if args.site_name:
            for site in existing_sites:
                if site["hostname"] == args.site_name:
                    current_site = site
                    break
        else:
            print_output("site_name_error")
        if current_site:
            current_site.pop("hash")
            current_site.pop("ssl_enabled")
            current_site.pop("ssl_blob")
            payload["site"] = current_site

            if args.backend:
                payload["site"]["backend"][0][0] = args.backend
            if args.blocking_types:
                site_blocking_types = args.blocking_types.replace(" ", "").split(",")
                for block_type in site_blocking_types:
                    if block_type.lower() == "manual":
                        payload["site"]["manual_action_blocking"] = True
                    elif block_type.lower() == "risk":
                        payload["site"]["risk_based_blocking"] = True
                    elif block_type.lower() == "request":
                        payload["site"]["request_blocking"] = True
            if args.http2:
                payload["site"]["http2_enabled"] = True
            if args.ssl_redirect:
                payload["site"]["ssl_redirect"] = True
            if args.ssl_protocols:
                payload["site"]["ssl_protocols"] = args.ssl_protocols
            if args.ssl_ciphers:
                payload["site"]["ssl_ciphers"] = args.ssl_ciphers
            if args.ssl and args.ssl.lower() == "true" and args.cert:
                with open(args.cert) as cert_file:
                    cert = cert_file.read()
                    payload["site"]["ssl_enabled"] = True
                    payload["site"]["ssl_blob"] = cert
            elif args.ssl and args.cert is None:
                print_output("cert_error")
            elif args.cert and args.ssl is None:
                print_output("ssl_true_error")
            
            if args.commit:
                update_site, err = txapi.sites(payload)
                if err is not None:
                    quit("Error: %s\n could not update site!" % (err))
                print(update_site)
            else:
                print_output("dry_run", args.site_name, "updated")
        else:
            print_output("site_error", args.site_name)

    elif args.action == "bulk_add":
        if args.bulk_file:
            bulk_file = csv.reader(open(args.bulk_file))
            payload = {}
            payload["command"] = "new"
            payload["customer_name"] = args.customer
            payload["site"] = {}
            payload["site"]["isEnabled"] = True
            payload["site"]["backend"] = [[ "", True]]
        else:
            print_output("bulk_file_error", "added")
        if args.ssl and args.ssl.lower() == "true" and args.cert:
            with open(args.cert) as cert_file:
                cert = cert_file.read()
                payload["site"]["ssl_enabled"] = True
                payload["site"]["ssl_blob"] = cert
        elif args.ssl and args.cert is None:
            print_output("cert_error")
        elif args.cert and args.ssl is None:
            print_output("ssl_true_error")
        if args.http2:
            payload["site"]["http2_enabled"] = True
        if args.ssl_redirect:
            payload["site"]["ssl_redirect"] = True
        for site in bulk_file:
            payload["site"]["hostname"] = site[0]
            payload["site"]["backend"][0][0] = site[1]
            blocking_modes = site[2].split(';')
            for block_type in blocking_modes:
                if block_type.lower() == "manual":
                    payload["site"]["manual_action_blocking"] = True
                elif block_type.lower() == "risk":
                    payload["site"]["risk_based_blocking"] = True
                elif block_type.lower() == "request":
                    payload["site"]["request_blocking"] = True
            if len(site) == 4 and payload["site"]["ssl_enabled"] is None:
                payload["site"]["ssl_enabled"] = True
                payload["site"]["ssl_blob"] = site[3]
            
            #Add site and return results
            if args.commit:
                bulk_new_site = txapi.sites(payload)
                print(bulk_new_site)
                risk = False
                request = False
                manual = False
                continue
            else:
                print_output("dry_run", payload["site"]["hostname"], "added")

    elif args.action == "bulk_update":
        payload = {}
        payload["command"] = "update"
        payload["customer_name"] = args.customer
        payload["site"] = {}
        if args.bulk_file:
            bulk_file = csv.reader(open(args.bulk_file))
            for bulk_site in bulk_file:
                current_site = {}
                for site in existing_sites:
                    if site["hostname"] == bulk_site[0]:
                        current_site = site
                        payload["name"] = bulk_site[0]
                        break
                if current_site:
                    current_site.pop("hash")
                    current_site.pop("ssl_enabled")
                    current_site.pop("ssl_blob")
                    payload["site"] = current_site
                    if args.backend:
                        payload["site"]["backend"][0][0] = args.backend
                    if args.blocking_types:
                        site_blocking_types = args.blocking_types.replace(" ", "").split(",")
                        for block_type in site_blocking_types:
                            if block_type.lower() == "manual":
                                payload["site"]["manual_action_blocking"] = True
                            elif block_type.lower() == "risk":
                                payload["site"]["risk_based_blocking"] = True
                            elif block_type.lower() == "request":
                                payload["site"]["request_blocking"] = True
                    if args.http2:
                        payload["site"]["http2_enabled"] = True
                    if args.ssl_redirect:
                        payload["site"]["ssl_redirect"] = True
                    if args.ssl_protocols:
                        payload["site"]["ssl_protocols"] = args.ssl_protocols
                    if args.ssl_ciphers:
                        payload["site"]["ssl_ciphers"] = args.ssl_ciphers
                    if args.ssl and args.ssl.lower() == "true" and args.cert:
                        with open(args.cert) as cert_file:
                            cert = cert_file.read()
                            payload["site"]["ssl_enabled"] = True
                            payload["site"]["ssl_blob"] = cert
                    elif args.ssl and args.cert is None:
                        print_output("cert_error")
                    elif args.cert and args.ssl is None:
                        print_output("ssl_true_error")
                    
                    if args.commit:
                        update_site, err = txapi.sites(payload)
                        if err is not None:
                            quit("Error: %s\n could not update site!" % (err))
                        print(update_site)
                    else:
                        print_output("dry_run", site["hostname"], "updated")
                
                else:
                    print_output("site_error", bulk_site[0])
        else:
            print_output("bulk_file_error", "updated")
    else:
        print_output("action_error")

if __name__ == "__main__":
    main()
