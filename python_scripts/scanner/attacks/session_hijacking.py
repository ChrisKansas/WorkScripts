import random
import requests
from time import sleep

# make a request to /?target=your-authenticated-page
def session_hijacking(target, source_ip, user_agent, **kwargs):

    hijack_ips = [
                     '11.32.22.11',
                     '11.32.22.12',
                     '11.32.22.13',
                     '11.32.22.13',
                     '11.32.22.14'
                 ]

    cookies = {'JSESSIONID': '10295818238745'}

    headers = {'User-Agent': user_agent,
               'True-Client-IP': str(source_ip),
               'X-ThreatX-Scan': 'session_hijacking'
              }

    headers_hijack = {'User-Agent': user_agent,
               'True-Client-IP': random.choice(hijack_ips),
               'X-ThreatX-Scan': 'session_hijacking'
              }

    response = requests.get(target + "/?target=your-authenticated-page", headers=headers, cookies=cookies).status_code
    sleep(5)
    response = requests.get(target + "/?target=your-authenticated-page", headers=headers_hijack, cookies=cookies).status_code

    return("session_hijacking: made duplicate JSESSIONID requests to /?target=your-authenticated-page")
