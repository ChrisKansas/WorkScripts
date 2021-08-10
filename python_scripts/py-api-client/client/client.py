""""
ThreatX API Python Client
"""
import requests
import furl
import json
from json import JSONDecodeError

class Client:

    def __init__(self, base_url, api_key):
        """
        * `base_url` - Base URL of the API Server ie. x.threatx.io/tx_api
        * `api_key` - AuthApiKey for user you wish to use
        """
        self.base_url = furl.furl(base_url)
        self.api_key = api_key
        self.session_token = None

    def login(self):
        """ Login to the API server with an AuthApiKey"""
        err = None

        url = self.base_url.copy().join('/tx_api/v1/login').url
        data = {'command': 'login', 'api_token': self.api_key}

        r = requests.post(url, json=data)

        try:
            body = r.json()
            if body['Ok']['status'] is True:
                self.session_token = body['Ok']['token']
            else:
                err = body['Ok']['status']
                return err
        except KeyError as exp:
            print(exp)
            print(r.text)
        except JSONDecodeError as e:
            print(r.text)
            raise e


    def auth(self, payload):
        response = {}
        err = None

        url = "%sauth" % (self.base_url)

        if payload['command'] in ['issue_password_reset', 'redeem_password_reset']:

            auth = { 'token': self.session_token}
            r = requests.post(url, json={**auth, **payload})

            if 'Ok' in r.json():
                response = r.json()['Ok']

            else:
                err = r.json()['Error']

        else:
            err = "command '%s' not defined" % (payload['command'])

        return response, err


    # customers api endpoint
    def customers(self,payload):
        response = {}
        err = None

        url = "%scustomers" % (self.base_url)

        if payload['command'] in ['list','list_all','new','get','update','delete',
                                  'list_api_keys','new_api_key','delete_api_key',
                                  'get_customer_config', 'set_customer_config' ]:

            auth = { 'token' : self.session_token }
            r = requests.post(url, json={**auth, **payload})

            if 'Ok' in r.json():
                response = r.json()['Ok']

            else:
                err = r.json()['Error']

        else:
            err = "command '%s' not defined" % (payload['command'])

        return response, err


    # users api endpoint
    def users(self,payload):
        response = {}
        err = None

        url = "%susers" % (self.base_url)

        if payload['command'] in ['list','new','get','update','delete',
                                  'get_api_key']:

            auth = { 'token' : self.session_token }
            r = requests.post(url, json={**auth, **payload})

            if 'Ok' in r.json():
                response = r.json()['Ok']

            else:
                err = r.json()['Error']

        else:
            err = "command '%s' not defined" % (payload['command'])

        return response, err


    # sites api endpoint
    def sites(self,payload):
        response = {}
        err = None

        self.base_url.path.segments[1] = 'v2'

        url = "%ssites" % (self.base_url)
        
        if payload['command'] in ['list','new','get','delete','update',
                                  'unset']:

            auth = { 'token' : self.session_token }
            r = requests.post(url, json={**auth, **payload})
            if 'Ok' in r.json():
                response = r.json()['Ok']
            else:
                err = r.json()['Error']

        else:
            err = "command '%s' not defined" % (payload['command'])

        return response, err

    # apikeys api endpoint
    def apikeys(self,payload):
        response = {}
        err = None
        
        self.base_url.path.segments[1] = 'v2'

        url = "%sapikeys" % (self.base_url)

        if payload['command'] in ['list','new','update','revoke','update']:

            auth = { 'token' : self.session_token }
            r = requests.post(url, json={**auth, **payload})
            if 'Ok' in r.json():
                response = r.json()['Ok']
            else:
                err = r.json()['Error']

        else:
            err = "command '%s' not defined" % (payload['command'])

        return response, err


    # templates api endpoint
    def templates(self,payload):
        response = {}
        err = None

        url = "%stemplates" % (self.base_url)

        if payload['command'] in ['set','get','delete']:

            auth = { 'token' : self.session_token }
            r = requests.post(url, json={**auth, **payload})

            if 'Ok' in r.json():
                response = r.json()['Ok']
            else:
                err = r.json()['Error']

        else:
            err = "command '%s' not defined" % (payload['command'])

        return response, err


    # sensors api endpoint
    def sensors(self,payload):
        response = {}
        err = None

        url = "%ssensors" % (self.base_url)

        if payload['command'] in ['list','tags']:

            auth = { 'token' : self.session_token }
            r = requests.post(url, json={**auth, **payload})

            if 'Ok' in r.json():
                response = r.json()['Ok']
            else:
                err = r.json()['Error']

        else:
            err = "command '%s' not defined" % (payload['command'])

        return response, err


    # services api endpoint
    def services(self,payload):
        response = {}
        err = None

        url = "%sservices" % (self.base_url)

        if payload['command'] in ['list']:

            auth = { 'token' : self.session_token }
            r = requests.post(url, json={**auth, **payload})

            if 'Ok' in r.json():
                response = r.json()['Ok']
            else:
                err = r.json()['Error']

        else:
            err = "command '%s' not defined" % (payload['command'])

        return response, err


    # entities api endpoint
    def entities(self,payload):
        response = {}
        err = None

        url = "%sentities" % (self.base_url)

        if payload['command'] in ['list','show',
                                  'state_changes','risk_changes',
                                  'notes','new_note',
                                  'reset', 'block_entity',
                                  'blacklist_entity', 'whitelist_entity',
                                  'watch_entity']:

            auth = { 'token' : self.session_token }
            r = requests.post(url, json={**auth, **payload})

            if 'Ok' in r.json():
                response = r.json()['Ok']
            else:
                err = r.json()['Error']

        else:
            err = "command '%s' not defined" % (payload['command'])

        return response, err


    # metrics api endpoint
    def metrics(self,payload):
        response = {}
        err = None

        url = "%smetrics" % (self.base_url)

        if payload['command'] in ['request_stats_by_hour','request_stats_by_minute',
                                  'match_stats_by_hour']:

            auth = { 'token' : self.session_token }
            r = requests.post(url, json={**auth, **payload})

            if 'Ok' in r.json():
                response = r.json()['Ok']

                # enrich data (hostname)
                if "hostnames" in payload:
                    for metric in response:
                        metric['hostname'] = payload['hostnames']

                # enrich data (customer_name)
                if "customer_name" in payload:
                    for log in response:
                        log['customer'] = payload['customer_name']

            else:
                err = r.json()['Error']

        else:
            err = "command '%s' not defined" % (payload['command'])

        return response, err


    # subscriptions api endpoint
    def subscriptions(self,payload):
        response = {}
        err = None

        url = "%ssubscriptions" % (self.base_url)

        if payload['command'] in ['save','delete','list','enable','disable']:

            auth = { 'token' : self.session_token }
            r = requests.post(url, json={**auth, **payload})

            if 'Ok' in r.json():
                response = r.json()['Ok']
            else:
                err = r.json()['Error']

        else:
            err = "command '%s' not defined" % (payload['command'])

        return response, err


    # logs api endpoint
    def logs(self,payload):
        response = {}
        err = None

        url = "%slogs" % (self.base_url)

        if payload['command'] in ['events','entities','blocks','actions',
                                  'matches','rule_hits','sysinfo', 'audit_log']:

            auth = { 'token' : self.session_token }
            r = requests.post(url, json={**auth, **payload})

            if 'Ok' in r.json():
                response = r.json()['Ok']

                # enrich data (customer_name)
                if "customer_name" in payload:
                    for log in response:
                        log['customer'] = payload['customer_name']

            else:
                err = r.json()['Error']

        else:
            err = "command '%s' not defined" % (payload['command'])

        return response, err


    # logs v2 api endpoint
    def logs_v2(self,payload):
        response = {}
        err = None
        
        self.base_url.path.segments[1] = 'v2'

        url = "%slogs" % (self.base_url)

        if payload['command'] in ['block_events','match_events','audit_events']:

            auth = { 'token' : self.session_token }
            r = requests.post(url, json={**auth, **payload})

            if 'Ok' in r.json():
                response = r.json()['Ok']

            else:
                err = r.json()['Error']

        else:
            err = "command '%s' not defined" % (payload['command'])

        return response, err


    # lists api endpoint
    def lists(self,payload):
        response = {}
        err = None

        url = "%slists" % (self.base_url)

        if payload['command'] in ['list_blacklist','list_blocklist','list_whitelist','list_ignorelist',
                                  'new_blacklist','new_blocklist','new_whitelist','new_ignorelist',
                                  'get_blacklist','get_blocklist','get_whitelist','get_ignorelist',
                                  'delete_blacklist','delete_blocklist','delete_whitelist','delete_ignorelist',
                                  'ip_to_link','bulk_new_whitelist','bulk_delete_whitelist','bulk_new_blacklist',
                                  'bulk_delete_blacklist','bulk_new_blocklist','bulk_delete_blocklist']:

            auth = { 'token' : self.session_token }
            r = requests.post(url, json={**auth, **payload})
            if payload['command'] == 'bulk_new_blacklist':
                if 'Ok' in r.json():
                    response = "IPs added!"
                else:
                    err = r.json()['Error']
            else:   
                if 'Ok' in r.json():
                    response = r.json()['Ok']
                else:
                    err = r.json()['Error']

        else:
            err = "command '%s' not defined" % (payload['command'])

        return response, err


    # rules api endpoint
    def rules(self,payload):
        response = {}
        err = None

        url = "%srules" % (self.base_url)

        if payload['command'] in ['list_customer_rules','list_whitelist_rules','list_profiler_rules','list_common_rules',
                                  'new_customer_rule','new_whitelist_rule','new_common_rule',
                                  'update_customer_rule','update_whitelist_rule','update_profiler_rule','update_common_rule',
                                  'get_customer_rule', 'get_whitelist_rule', 'get_profiler_rule', 'get_common_rule',
                                  'delete_customer_rule','delete_whitelist_rule','delete_profiler_rule','delete_common_rule',
                                  'validate_rule']:

            auth = { 'token' : self.session_token }
            r = requests.post(url, json={**auth, **payload})

            if 'Ok' in r.json():
                response = r.json()['Ok']
            else:
                err = r.json()['Error']

        else:
            err = "command '%s' not defined" % (payload['command'])

        return response, err

    def make_request(self, path: str, payload: dict):
        """ Make a generic request to the API
        """
        url = self.base_url.copy().join(path).url
        print(url)
        # add current session token
        payload['token'] = self.session_token
        resp = requests.post(url, json=payload)
        try:
            resp.raise_for_status()
            body = resp.json()
        except requests.exceptions.HTTPError as e:
            print(resp.text)
            raise e
        except JSONDecodeError as e:
            print(resp.text)
            raise e
        if 'Ok' in body and body['Ok']:
            return body['Ok']
        if 'Error' in body and body['Error']:
            raise Exception(body['Error'])

