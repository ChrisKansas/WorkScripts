import requests, json, csv, sys, re

#NEEDS TO TAKE FILE LOCATION FOR CERT AND SITE LIST
#SSL and site enabled SETTINGS SHOULD NOT BE ADJUSTED UNLESS SPECIFIED

# Individual API Token Input
api_key = sys.argv[1] 

# API Endpoints
login_endpoint = "https://provision.threatx.io/tx_api/v1/login"
sites_endpoint = "https://provision.threatx.io/tx_api/v2/sites"

# Common API Header Input
api_headers = {'Content-Type': "application/json"}

# Define Input Variables
bulk_sites_file = csv.reader(open('bulk_sites.csv'))


# Login to API and Receive API Token
def api_login_pull(input_token):
    login_payload = "{\n\t\"command\":\"login\",\n\t\"api_token\":\"%s\"\n}" % input_token
    login_response = requests.request("POST", login_endpoint, data=login_payload, headers=api_headers)
    login_json_response = json.loads(login_response.text)
    temp_threatx_token = login_json_response['Ok']['token']
    return temp_threatx_token

def pull_site_obj(input_token, input_customer_name, input_site_name):
    pull_site_obj_payload ='{ "command":"get", "token":"%s", "customer_name":"%s", "name":"%s" }' % \
            (input_token, input_customer_name, input_site_name)
    pull_site_response = requests.request("POST", sites_endpoint, data=pull_site_obj_payload,headers=api_headers)
    json_response = json.loads(pull_site_response.text)
    return json.dumps(json_response['Ok']['backend'])

# Add A Site to a Customer
def update_site(input_token, input_customer_name, input_site_name, input_backend, input_ssl_blob):
    update_site_payload = "{\"command\":\"update\",\"token\":\"%s\",\"customer_name\":\"%s\"," \
            "\"name\": \"%s\",\"site\":{\"hostname\":\"%s\",\"backend\":%s," \
            "\"isEnabled\":true,\"ssl_enabled\":true,\"ssl_blob\":\"%s\"} }" % \
                       (input_token, input_customer_name, input_site_name, input_site_name, str(input_backend).replace("'",'"'), input_ssl_blob)
    update_site_response = requests.request("POST", sites_endpoint, data=update_site_payload, headers=api_headers)
    update_site_json_response = json.loads(update_site_response.text)
    return update_site_json_response


# Define threatx_token
threatx_token = api_login_pull(api_key)

# Loop through rows in CSV and create sites in ThreatX, one per line in the CSV
ssl_blob = open("./cert_provided","r")
if ssl_blob.mode == 'r':
    blob = re.sub(r"\n+", "\\\\n", ssl_blob.read())
for site in bulk_sites_file:
    customer_name = "soclab1"
    site_name = site[0]
    print(update_site(threatx_token, customer_name, site_name, pull_site_obj(threatx_token, customer_name, site_name),blob.strip()))
