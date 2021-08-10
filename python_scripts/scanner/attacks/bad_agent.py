import random
import requests

# make a request with a bad user-agent
def bad_agent(target, source_ip, **kwargs):

    bad_user_agents = ['Wget', 'Medusa', 'Arachni', 'sqlmap', 'python-httplib2', 'okhttp', 'java/7.1', 'Nikto',
                       'w3af', 'curl', 'WinHTTP', 'MJ12bot', 'panscient.com', 'Sogou', 'Java/1.8.0', 'YisouSpider',
                       'Mozilla/5.0 (Windows NT 5.1; rv:7.0.1) Gecko/20100101 Firefox/7.0.1',
                       'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.57 Safari/537.36'
                      ]

    headers = {'User-Agent': random.choice(bad_user_agents),
               'True-Client-IP': str(source_ip)
              }

    response=requests.get(target+"/",headers=headers).status_code
    return("bad_agent: got {} with {}".format(response,headers['User-Agent']))
