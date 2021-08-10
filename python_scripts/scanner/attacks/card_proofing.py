import random
import requests
from time import sleep

# send creds from a list to /?target=your-card-transation-page
def card_proofing(target, source_ip, user_agent, **kwargs):

    #card info to try
    card_list = [
                    { 'cc': '4291019240291532', 'type': 'Visa', 'zip': '30982', 'cvv': '912' },
                    { 'cc': '5424183492095820', 'type': 'MasterCard', 'zip': '91082', 'cvv': '215' },
                    { 'cc': '5439413569206869', 'type': 'MasterCard', 'zip': '43827', 'cvv': '382' },
                    { 'cc': '4954378135634567', 'type': 'Visa', 'zip': '57842', 'cvv': '275' },
                    { 'cc': '4229201545656384', 'type': 'Visa', 'zip': '39653', 'cvv': '791' },
                    { 'cc': '4223460154475367', 'type': 'Visa', 'zip': '59453', 'cvv': '571' },
                    { 'cc': '4259201541509315', 'type': 'Visa', 'zip': '79254', 'cvv': '137' },
                    { 'cc': '4723692015638424', 'type': 'Visa', 'zip': '94425', 'cvv': '168' },
                    { 'cc': '5534357941353456', 'type': 'MasterCard', 'zip': '43345', 'cvv': '794' },
                    { 'cc': '5439432211643248', 'type': 'MasterCard', 'zip': '11094', 'cvv': '983' },
                    { 'cc': '5733469164324836', 'type': 'MasterCard', 'zip': '40912', 'cvv': '910' }
                ]


    headers = {'User-Agent': user_agent,
               'True-Client-IP': str(source_ip),
               'Content-Type': 'application/x-www-form-urlencoded',
               'X-ThreatX-Scan': 'card_proofing'
              }

    count=random.randint(5,10)

    for i in range(count):

        card = random.choice(card_list)

        attack = {
                  "method": "POST",
                  "url": "{}/?target=your-card-transation-page".format(target),
                  "payload": {"cc": card['cc'], "type": card['type'], "zip": card['zip'], "cvv": card['cvv']}
                  }
        response = requests.request(attack['method'], attack['url'], headers=headers, data=attack['payload']).status_code

        sleep(5)

    return("card_proodinf: sent {} cards to {}/?target=your-card-transation-page".format(count,target))
