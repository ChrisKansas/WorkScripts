import random
import requests

# make a request for a shady uri
def shady_uri(target, source_ip, user_agent, **kwargs):

    uri_list = ['phpMyAdmin', 'wp-content', 'phpSlash', 'apache-rproxy-status', 'wwwstats', 'jenkins', 'htaccess',
                'wp-plugin', 'wp-config.php', 'wp-includes', 'wp-admin',
                'wp-content/plugins/lazy-content-slider/lzcs_admin.php']

    headers = {'User-Agent': user_agent,
               'True-Client-IP': str(source_ip)
              }

    bad_uri = random.choice(uri_list)
    response = requests.get(target + "/" + bad_uri, headers=headers).status_code
    return("shady_uri: got {} with /{}".format(response,bad_uri))
