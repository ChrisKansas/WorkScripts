# py-api-client

This is a basic client library for the [ThreatX provisioning API](https://support.threatx.com/hc/en-us/articles/360000661851-API-Reference).

## requirements
* python 3 (3.5+)
* requests, json

You can install requirements for the lib & example.py script with `pipenv install`

## usage
1. Import Client into your script: `from client import Client`
1. Create a new Client: `txapi = Client('URL','API_KEY')`
1. Call functions like: `txapi.login()`

Basic error checking is perfomed client side, but mostly relies on API errors -- see [API Reference](https://support.threatx.com/hc/en-us/articles/360000661851-API-Reference).

## example.py
The [example.py](example.py) script is included to provide sample code for the library.
It implements login and a few API calls with `--command`.

Run with `pipenv run python example.py -h`
```
usage: example.py [-h] --api_key API_KEY [--url URL] --command COMMAND

optional arguments:
  -h, --help         show this help message and exit
  --api_key API_KEY  threatx provisioning API key
  --url URL          threatx provisioning API url
                     (default: https://provision.threatx.io/tx_api/v1/)
  --command COMMAND  action to perform:
                     list_customers     print all customer names
                     get_logs_events    print logs events for all customers
```

