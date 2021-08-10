import requests

# an example attack
def api_demo_lrq(target, source_ip, user_agent, **kwargs):

    # True-Client-IP needs to be set in order to spoof source ip.
    headers = {'User-Agent': user_agent,
               'True-Client-IP': str(source_ip),
               'Content-Type': 'application/json'
              }

    # send the request and get a status_code back
    ret = ""
    for i in range(5):

        attack = {
                  "method": "POST",
                  "url": "{}/api/v1/shippingamount".format(target),
                  "payload": {}
                  }
        response = requests.request(attack['method'], attack['url'], headers=headers, data=attack['payload']).status_code
        ret += "api_demo_lrq: got {} with {}\n".format(response,attack['url'])

    # return a string showing attack status
    return(ret)
