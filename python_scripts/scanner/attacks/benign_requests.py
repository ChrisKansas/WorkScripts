import random
import requests
from time import sleep

# make some perfectly benign requests to /
def benign_requests(target, source_ip, user_agent, **kwargs):

    headers = {'User-Agent': user_agent,
               'True-Client-IP': str(source_ip)
              }

    count = 75

    for i in range(count):
        response = requests.get(target + "/", headers=headers).status_code
        sleep(random.randint(0,1))

    return("benign_requests: made {} GET requests to /".format(count))
