#!/usr/bin/python3

# Script to take IP ranges and list out individual IPs

import sys, ipaddress

listoips=sys.argv[1]

f=open(listoips, "r")

list_of_ips = []

for line in f.readlines():
    if "/13" in line:
        print("/13")
    elif "/14" in line:
        print("/14")
    elif "/15" in line:
        print("/15")
    
    #net = list(ipaddress.ip_network(line.strip(), False).hosts())
    #for ip in net:
    #    list_of_ips.append(ip)

#for ip in list_of_ips:
#    print(ip)
