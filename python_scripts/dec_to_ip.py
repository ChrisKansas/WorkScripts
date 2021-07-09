#!/usr/bin/python3
import socket, struct, sys
listoips=sys.argv[1]
f=open(listoips, "r")
for blah in f.readlines():
    count_and_ip=blah.strip().split(' ')
    ip=socket.inet_ntoa(struct.pack('!L', int(count_and_ip[0])))
    count=count_and_ip[0]
    print(ip+': '+count)
