import requests

# an example attack
def example_attack(target, source_ip, user_agent, **kwargs):

    # the uri we're going to request
    uri = 'example.html'

    # True-Client-IP needs to be set in order to spoof source ip.
    headers = {'User-Agent': user_agent,
               'True-Client-IP': str(source_ip)
              }

    # send the request and get a status_code back
    response = requests.get(target + "/" + uri, headers=headers).status_code

    # return a string showing attack status
    return("example_attack: got {} with /{}".format(response,uri))
