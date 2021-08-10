# Scanner

Scanner is a framework for generating web attack traffic.

To run existing attacks, use the [docker image](#docker-image) below.

## runner.py
Wrapper for targeting, selecting sources, and launching attacks.

```
usage: runner.py [-h] [-l] [-t TARGET] [-ft TARGETS] [-s SOURCE] [-fs SOURCES]
                 [-a ATTACK] [-fa ATTACKS] [-c COUNT] [-w WAIT] [-ch CHANCE]

runner.py - wrapper for targeting, selecting sources, and launching attacks

optional arguments:
  -h, --help            show this help message and exit
  -l, --list_attacks    list all loaded attack modules
  -t TARGET, --target TARGET
                        target host
  -ft TARGETS, --targets TARGETS
                        read targets from file in format:
                        scheme://hostname:path_prefix,weight
  -s SOURCE, --source SOURCE
                        source ip address
  -fs SOURCES, --sources SOURCES
                        read source ips from file in format: 0.0.0.0/0,weight
  -a ATTACK, --attack ATTACK
                        attack to perform
  -fa ATTACKS, --attacks ATTACKS
                        read attacks from file in format: attackname,weight
  -c COUNT, --count COUNT
                        number of times to perform an attack. format: integer
                        or range nn-nn
  -w WAIT, --wait WAIT, --sleep WAIT
                        number of seconds to wait between performing attacks.
                        format: integer or range nn-nn
  -ch CHANCE, --chance CHANCE
                        chance to fire. format: integer 0-100
```

## attacks
Modular web attack scripts.

To list all loaded attacks: `python runner.py -l`

To perform the specified attack: `python runner.py -t <target> -a <attack_name>`

### creating new attacks
An `attack` is one or more HTTP requests which represent an attempt to exploit some target web application. A new module should be self-contained, including any/all possible payloads, attack vectors, etc.

To register new attacks:
1. Create a new .py file in the [attacks](attacks) directory
2. Import in [attacks/__init__.py](attacks/__init__.py)

The `runner.py` provides the following variables to an attack module when called:
- `target` (string, http/https hostname + path)
- `source_ip` (string, IPv4 address)
- `user_agent` (string, a 'normal', browser-like User-Agent header)

In order to spoof the source IP, the attack needs to set `True-Client-IP` header before making the request
```
headers = {
           'True-Client-IP': str(source_ip)
          }
```

`runner.py` expects the attack to return a single string. Something like: `"bad_agent: got {} with {}".format(response,headers['User-Agent']))`

See the [`example_attack.py`](attacks/example_attack.py).

## Installation (development)

scanner currently requires python 3.x and a number of modules. The easiest way to install dependencies _mostly anywhere_ is with `pyenv` and `pipenv` like so:

```
#install pyenv
curl -L https://github.com/pyenv/pyenv-installer/raw/master/bin/pyenv-installer | bash

#install pipenv
sudo pip install pipenv

#install dependencies
pipenv run pip install --upgrade pip
pipenv install

#run it!
pipenv run python runner.py --target www.securedmz.com
```

## config & operation
Basic config (designed to run against threatx demo environment) is located in the [config/](config) directory.

An example crontab is also located in the directory -- [config/crontab](config/crontab)

## Docker image

Use Docker to create a consistent, portable python environment for the runner & call into the container to launch attacks.

### build the container
```
git clone https://github.com/ThreatX/threatx-scans && cd threatx-scans/scanner
docker image build . -t  registry.threatx.io/threatx-scans-scanner:latest
```

### run the container
```
docker run -id --name scanner --restart always registry.threatx.io/threatx-scans-scanner:latest
```
or run [`start-scanner.sh`](start-scanner.sh)

### call the runner
Example:
```
docker exec scanner sh -c 'python runner.py -ft config/targets -fs config/sources -a benign_requests -c 8-10 2>&1'
```
