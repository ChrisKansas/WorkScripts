import random
import requests

# make a request with a known bot user-agent from several IPs
def botnet_agent(target, source_ip, **kwargs):

    ips = [
             '14.32.22.11',
             '14.32.22.12',
             '14.32.22.13',
             '14.32.22.13',
             '14.32.22.14',
             '14.32.22.15',
             '14.32.22.16',
             '14.32.22.17',
             '14.32.22.18',
             '14.32.22.19',
             '14.32.22.20',
             '14.32.22.21',
             '14.32.22.22',
             '14.32.22.23',
             '14.32.22.24',
             '14.32.22.25'
         ]

    count=random.randint(3,5)

    for i in range(count):

        headers = {'User-Agent': 'MJ12bot',
                   'True-Client-IP': random.choice(ips)
                  }

        response=requests.get(target+"/",headers=headers).status_code


    return("botnet_agent: sent {} requests with User-Agent '{}'".format(count,headers['User-Agent']))
