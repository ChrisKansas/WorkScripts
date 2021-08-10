import requests
import json

# an example attack
def api_demo_benign_requests(target, source_ip, user_agent, **kwargs):

    # the uri we're going to request
    uri = '/api/v1/items'

    # True-Client-IP needs to be set in order to spoof source ip.
    headers = {'User-Agent': user_agent,
               'True-Client-IP': str(source_ip)
              }

    # get a list of items
    items_list = requests.get(target + uri, headers=headers)
    
    # send the request and get a status_code back
    ret = ""
    for item in items_list.json():
        item_uri = target + uri + "/" + str(item)
        response = requests.get(item_uri, headers=headers).status_code
        ret += "api_demo_benign_requests: got {} with {}\n".format(response,item_uri)
    return(ret)
