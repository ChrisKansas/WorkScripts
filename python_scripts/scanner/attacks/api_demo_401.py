import requests

# an example attack
def api_demo_401(target, source_ip, user_agent, **kwargs):

    # the uri we're going to request
    uri = '/api/v1/orders'

    # True-Client-IP needs to be set in order to spoof source ip.
    headers = {'User-Agent': user_agent,
               'True-Client-IP': str(source_ip)
              }

    # send the request and get a status_code back
    ret = ""
    for i in range(15):
        response = requests.get(target + uri, headers=headers).status_code
        ret += "api_demo_401: got {} with {}\n".format(response,uri)
    return(ret)
