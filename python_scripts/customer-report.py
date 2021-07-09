#Tool for reporting on customer features and settings

import argparse, textwrap, json, hashlib, sys, os
sys.path.append('../py-api-client/client')
from client import Client

#Arguments
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

    # get customer WAF settings
    customer, err = txapi.customers({'command':'get','name':args.customer})
    if err is not None:
        quit("Error: %s\ncould not get customer" % (err))
        
    # get customer rules information
    customer_rules, err = txapi.rules({'command':'list_customer_rules', 'customer_name':args.customer})
    if err is not None:
        quit("Error: %s\ncould not get customer rules." % (err))

    # get customer subscription information
    customer_subs, err = txapi.subscriptions({'command':'list', 'customer_name':args.customer})
    if err is not None:
        quit("Error: %s\ncould not get customer rules." % (err))
    
    # get customer subscription information
    customer_users, err = txapi.users({'command':'list', 'customer_name':args.customer})
    if err is not None:
        quit("Error: %s\ncould not get customer rules." % (err))
    
    # get customer subscription information
    customer_apikeys, err = txapi.apikeys({'command':'list', 'customer_name':args.customer})
    if err is not None:
        quit("Error: %s\ncould not get customer rules." % (err))
    
    # get customer sites information
    customer_sites, err = txapi.sites({'command':'list', 'customer_name':args.customer})
    if err is not None:
        quit("Error: %s\ncould not get customer rules." % (err))
    
    size = os.get_terminal_size()
    notifications = []
    log_emitters_enabled = []
    log_emitters_disabled = []
    users_2FA = []
    request_blocking_disabled = []
    risk_blocking_disabled = []
    static_caching_enabled = []
    dynamic_caching_enabled = []
    
    'static_caching_enabled' 
    'dynamic_caching_enabled'
    
    print("-" * int(size[0]))
    print("\n**********CUSTOMER INFO**********\n")
    print("Customer Name: %s" % args.customer)
    print("Contact Email: %s" % customer["contact_email"])
    print("Risk-Based Blocking Threshold: %s" % customer["autoblock_threshold"])
    print("Risk-Based Blocking Timeout: %s minutes" % str(int(customer["autoblock_timeout"]/60)))
    
    #GeoBlock Enabled Check
    for i, rule in enumerate(customer_rules):
        if "GeoBlock" in rule["description"]:
            print("Block Embargoed Countries Enabled: Yes")
            break
        elif i == (len(customer_rules)-1) and "GeoBlock" not in rule["description"]:
            print("Block Embargoed Countries Enabled: No")
    
    #TOR Nodes Block Enable Check
    for i, rule in enumerate(customer_rules):
        if "TOR" in rule["description"]:
            print("Block Tor Nodes Enabled: Yes")
            break
        elif i == (len(customer_rules)-1) and "TOR" not in rule["description"]:
            print("Block Tor Nodes Enabled: No")
    
    #Log Emitter/Notifications
    print("\n**********LOG EMITTER**********\n")
    if not customer_subs:
        print("Log Emitter Enabled: No")
        print("No subscriptions currently configured.")
    else:
        for item in customer_subs:
            if item["type"] == "notification":
                notifications.append(item["name"])
            elif item["type"] == "syslog": 
                if item["enabled"] == True:
                    log_emitters_enabled.append(item["name"])
                else:
                    log_emitters_disabled.append(item["name"])
        if not log_emitters_enabled and not log_emitters_disabled:
            print("Log Emitter Enabled: No")
            print("No log emitters currently configured.")
        elif log_emitters_enabled and log_emitters_disabled:
            print("Log Emitter Enabled: Yes")
            if len(log_emitters_enabled) > 1:
                print("Enabled Log Emitter Names: %s" % ", ".join(log_emitters_enabled))
            else:
                print("Enabled Log Emitter Name: %s" % ", ".join(log_emitters_enabled))
            if len(log_emitters_disabled) > 1:
                print("Disabled Log Emitter Names: %s" % ", ".join(log_emitters_disabled))
            else:
                print("Enabled Log Emitter Name: %s" % ", ".join(log_emitters_disabled))
        elif log_emitters_enabled and not log_emitters_disabled:
            print("Log Emitter Enabled: Yes")
            if len(log_emitters_enabled) > 1:
                print("Enabled Log Emitter Names: %s" % ", ".join(log_emitters_enabled))
            else:
                print("Enabled Log Emitter Name: %s" % ", ".join(log_emitters_enabled))
        elif log_emitters_disabled and not log_emitters_enabled:
            print("Log Emitter Enabled: No")
            if len(log_emitters_disabled) > 1:
                print("Disabled Log Emitter Names: %s" % ", ".join(log_emitters_disabled))
            else:
                print("Enabled Log Emitter Name: %s" % ", ".join(log_emitters_disabled))
        
        print("\n**********NOTIFICATIONS**********\n")
        if notifications:
            print("Number of Notifications: %s" % str(len(notifications)))
            if len(notifications) > 1:
                print("Notification Names: %s" % ", ".join(notifications))
            else:
                print("Notification Name: %s" % ", ".join(notifications))
        else:
            print("No notifications currently setup.")
    
    #SSO Enabled Check
    print("\n**********SSO**********\n")
    if customer["sso"] is not None:
        print("SSO Enabled: %s" % customer["sso"]["enabled"])
    else:
        print("SSO Enabled: No")
    
    #User 2FA Check
    print("\n**********USERS**********\n")
    if not customer_users:
        print("No users added for this customer.")
    else:
        for user in customer_users:
            if user["requires_totp_auth"] == False or user["requires_totp_auth"] == None:
                users_2FA.append(user["username"])
        if users_2FA:
            print("Users without 2FA Enabled: %s" % ", ".join(users_2FA))
        else:
            print("All users have 2FA Enabled.")

    #Api Keys Check
    print("\n********API KEYS********\n")
    if customer_apikeys:
        for i, key in enumerate(customer_apikeys):
            if i == (len(customer_apikeys)-1):
                print("API Keys Issued: Yes")
                print("Number of API Keys Issued: %s" % str(i+1))
    else:
        print("API Keys Issued: No")
    
    #Sites Risk/Request Blocking Check
    print("\n**********RISK & REQUEST BLOCKING**********\n")
    if customer_sites:
        for site in customer_sites:
            if site["request_blocking"] == False and site["risk_based_blocking"] == False:
                request_blocking_disabled.append(site["hostname"])
                risk_blocking_disabled.append(site["hostname"])
            elif site["request_blocking"] == False and site ["risk_based_blocking"] == True:
                request_blocking_disabled.append(site["hostname"])
            elif site["risk_based_blocking"] == False and site["request_blocking"] == True:
                risk_blocking_disabled.append(site["hostname"])
            else:
                continue
        if request_blocking_disabled:
            print("Number of sites without request-based blocking enabled: %s" % str(len(request_blocking_disabled)))
            print("Sites with risk-based blocking disabled: %s" % ", ".join(request_blocking_disabled))
        else:
            print("No sites without request-based blocking enabled.")
        print("\n")
        if risk_blocking_disabled:
            print("Number of sites without risk-based blocking enabled: %s" % str(len(risk_blocking_disabled)))
            print("Sites with risk-based blocking disabled: %s" % ", ".join(risk_blocking_disabled))
        else:
            print("No sites without risk-based blocking enabled.")
    else:
       print("No sites currently configured for this customer.") 
    
    #Sites Static/Dynamic Caching Check
    print("\n**********STATIC & DYNAMIC CACHING**********\n")
    if customer_sites:
        for site in customer_sites:
            if site["static_caching_enabled"] == True and site["dynamic_caching_enabled"] == True:
                static_caching_enabled.append(site["hostname"])
                dynamic_caching_enabled.append(site["hostname"])
            elif site["dynamic_caching_enabled"] == False and site["static_caching_enabled"] == True:
                static_caching_enabled.append(site["hostname"])
            elif site["static_caching_enabled"] == False and site["dynamic_caching_enabled"] == True:
                dynamic_caching_enabled.append(site["hostname"])
            else:
                continue
        if static_caching_enabled:
            print("Number of sites with static caching enabled: %s" % str(len(static_caching_enabled)))
            print("Sites with static caching enabled: %s" % ", ".join(static_caching_enabled))
        else:
            print("No sites with static caching enabled.")
        print("\n")
        if dynamic_caching_enabled:
            print("Number of sites with dynamic caching enabled: %s" % str(len(dynamic_caching_enabled)))
            print("Sites with dynamic caching enabled: %s" % ", ".join(dynamic_caching_enabled))
        else:
            print("No sites with dynamic caching enabled.")
    else:
       print("No sites currently configured for this customer.") 
    
    print("\n" + "-" * int(size[0]))

if __name__ == '__main__':
    main()
