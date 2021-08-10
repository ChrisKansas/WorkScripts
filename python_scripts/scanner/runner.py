#!/usr/bin/python
import sys, random, argparse
from time import gmtime, strftime, sleep
import requests
import ipaddress
import attacks

parser = argparse.ArgumentParser(description='runner.py - wrapper for targeting, selecting sources, and launching attacks')
parser.add_argument('-l','--list_attacks',
  help="list all loaded attack modules",
  action='store_true'
  )
parser.add_argument('-t','--target',
  help="target host",
  )
parser.add_argument('-ft','--targets',
  help="read targets from file in format: scheme://hostname:path_prefix,weight",
  )
parser.add_argument('-s','--source',
  help='source ip address'
  )
parser.add_argument('-fs','--sources',
  help="read source ips from file in format: 0.0.0.0/0,weight"
  )
parser.add_argument('-a','--attack',
  help='attack to perform'
  )
parser.add_argument('-fa','--attacks',
  help="read attacks from file in format: attackname,weight"
  )
parser.add_argument('-c','--count',
  help="number of times to perform an attack. format: integer or range nn-nn"
  )
parser.add_argument('-w','--wait', '--sleep',
  help="number of seconds to wait between performing attacks. format: integer or range nn-nn",
  default='0'
  )
parser.add_argument('-ch','--chance',
  help="chance to fire. format: integer 0-100",
  default='100'
  )

args = parser.parse_args()


# load a list of values from file in format: value,weight
def load_weighted_list(filename):
    values = {}

    with open(filename, 'r') as f:
        value_file = [line.rstrip() for line in f]

    for line in value_file:
        values[line.split(',')[0]] = int(line.split(',')[1])

    return values

# list all loaded attack modules
def list_attacks_module():
    attacks = []

    for module in sys.modules.keys():
        if module.startswith('attacks.'):
            attacks.append(module.split('attacks.')[1])

    return attacks

# pick a target from weighted list
def get_target(targets):

    # pick a target from targets (weighted)
    total = sum(weight for target, weight in targets.items())
    r = random.uniform(0, total)
    upto = 0

    for target, weight in targets.items():
        if upto + weight >= r:
            return target
        upto += weight

    return None


# pick a source IP from weighted list of CIDRs
def get_ip(sources):

    # pick a cidr from sources (weighted)
    total = sum(weight for source, weight in sources.items())
    r = random.uniform(0, total)
    upto = 0

    for source, weight in sources.items():
        if upto + weight >= r:
            cidr = ipaddress.ip_network(source)
            break
        upto += weight

    try:
        # pick an ip in cidr
        return random.choice(list(cidr.hosts()))
    except IndexError:
        # cidr is a /32, return it
        return cidr[0]


# pick an attack from weighted list
def get_attack(attacks):

    # pick a target from targets (weighted)
    total = sum(weight for attack, weight in attacks.items())
    r = random.uniform(0, total)
    upto = 0

    for attack, weight in attacks.items():
        if upto + weight >= r:
            return attack
        upto += weight

    return None


# get a random ip from a static list
def get_builtin_ip():

    ips = ['1.4.64.61', '1.4.69.10', '1.4.65.110', '1.4.74.11', '1.4.79.1', '1.4.75.107', '1.4.64.261',
           '1.4.89.221', '1.4.95.183', '1.4.94.111', '1.4.89.31', '1.4.95.107', '14.208.1.1', '14.208.100.11',
           '14.208.1.1', '14.208.11.22', '14.201.1.1', '14.208.130.11', '36.1.1.1', '36.4.100.11', '36.16.2.213',
           '36.1.16.223', '36.4.14.13', '27.225.130.11', '42.1.32.121', '42.1.32.110', '42.1.32.44', '42.1.32,49',
           '42.1.32.32', '42.1.32.200', '42.1.32.201', '42.1.32.222', '42.1.32.253', '42.1.32.2', '42.1.32.4',
           '27.125.226.23', '27.125.226.25', '27.125.226.28', '27.125.226.29', '1.125.227.11', '1.125.227.13',
           '1.125.227.15', '1.125.227.18', '1.125.227.19', '1.125.227.21', '1.125.227.23', '1.125.227.25',
           '102.3.212.21', '102.3.212.23', '102.3.212.24', '102.3.212.25', '102.3.212.26', '102.3.212.27',
           '105.92.212.37', '105.92.212.57', '105.92.212.59', '105.92.212.61', '105.92.212.71', '105.92.212.81',
           '105.92.212.87', '105.92.212.91', '105.92.212.126', '105.92.212.225', '105.92.212.72', '105.92.212.73',
           '181.4.212.21', '181.4.212.23', '181.4.212.24', '181.4.212.25', '181.4.212.26', '181.4.212.27',
           '181.33.212.28', '181.33.212.29', '181.33.212.121', '181.33.212.221', '181.33.212.34', '181.33.212.35',
           '181.33.212.37', '181.33.212.57', '181.33.212.59', '181.33.212.61', '181.33.212.71', '181.33.212.81',
           '200.154.212.21', '200.154.212.23', '200.154.212.24', '200.154.212.25', '200.154.212.26',
           '201.93.212.29', '201.93.212.121', '201.93.212.221', '201.93.212.34', '201.93.212.35', '201.93.212.37',
           '201.93.212.57', '201.93.212.59', '201.93.212.61', '201.93.212.71', '201.93.212.81', '201.93.212.87',
           '189.5.212.57', '189.5.212.59', '189.5.212.61', '189.5.212.71', '189.5.212.81', '189.5.212.87',
           '105.17.212.91', '105.17.212.126', '105.17.212.225', '105.17.212.72', '105.17.212.73']

    return random.choice(ips)


# get a random 'good' User-Agent from a list
def get_user_agent():

    user_agents = [
                   "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
                   "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36",
                   "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:64.0) Gecko/20100101 Firefox/64.0",
                   "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/17.17134",
                   "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Trident/6.0)",
                   "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
                   "Mozilla/5.0 (iPhone; CPU iPhone OS 12_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0 Mobile/15E148 Safari/604.1",
                   "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0.1 Safari/605.1.15"
                  ]

    return random.choice(user_agents)


def main():

    # print header
    print("{} - {}".format(strftime("%Y-%m-%dT%H:%M:%S", gmtime()),sys.argv[0]))
    print("------------")

    # print the list of attack modules
    if args.list_attacks:
        module_list = list_attacks_module()
        print("|-- Attack modules loaded ({}):\n|   |-- "
              .format(len(module_list))+'\n|   |-- '.join(module_list)
             )
        print("------------")
        sys.exit()

    # stop execution if 'chance to fire' doesn't hit.
    if random.randint(0,100) > int(args.chance):
        sys.exit("Chance {}/100 didn't hit! Aborting.".format(args.chance))

    # set a target (scheme://hostname:path_prefix)
    if args.target:
        target = args.target
        if not target.startswith('http'):
          target = 'http://' + target
    elif args.targets:
        targets = load_weighted_list(args.targets)
        target = get_target(targets)
    else:
        sys.exit('Error: you must set a target with --target or --targets')
    print("|-- Using target: {}".format(target))

    # pick a source ip address
    if args.source:
        source = args.source
    elif args.sources:
        sources = load_weighted_list(args.sources)
        source = get_ip(sources)
    else:
        source = get_builtin_ip()
    print("|-- Using source ip: {}".format(source))

    # pick the number of times to perform an attack
    if args.count:
        try:
            count = random.randint(
                                  int(args.count.split('-')[0]),
                                  int(args.count.split('-')[1])
                                  )
        except IndexError:
            count = int(args.count)
    else:
        count = random.randint(1, 3)
    print("|-- Performing attacks ({})".format(count))


    # perform one or more attacks
    for i in range(0,count):

        # pick an attack to perform
        if args.attack:
            attack = getattr(attacks, args.attack)
        elif args.attacks:
            attack_list = load_weighted_list(args.attacks)
            attack = getattr(attacks, get_attack(attack_list))
        else:
            attack = getattr(attacks, random.choice(list_attacks_module()))
        print("|   |-- ({}) Using attack: {}".format(i+1,attack.__name__))

        # perform the attack
        result = attack(
                       target=target,
                       source_ip=source,
                       user_agent=get_user_agent()
                       )
        for line in result.splitlines():
            print("|   |   |-- {}".format(line))

        # determine how long to wait between attacks
        try:
            wait = random.randint(
                                 int(args.wait.split('-')[0]),
                                 int(args.wait.split('-')[1])
                                 )
        except IndexError:
            wait = args.wait
        if wait:
            print("|   |   |-- Waiting before next attack ({}s)".format(wait))
            sleep(int(wait))

    # print footer
    print("------------")


if __name__ == "__main__":
    main()
