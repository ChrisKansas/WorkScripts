#!/usr/bin/python3

#Script takes IANA cipher name and translates to openSSL name for our use

import sys, requests

cipher_list = []
translated_list = []

#Checks if a file is being read in
if sys.argv[1] == "-f":
    ciphers = open(sys.argv[2], 'r').read()
    ciphers = ciphers.strip()
    ciphers = ciphers.split(',')
    for cipher in ciphers:
        cipher_list.append(cipher)
    for cipher in cipher_list:
        response = requests.get("https://ciphersuite.info/api/cs/" + cipher)
        name = response.json()[cipher]['openssl_name']
        translated_list.append(name)
    print(translated_list) #Prints out the translated ciphers
else:
    response = requests.get("https://ciphersuite.info/api/cs/" + sys.argv[1])
    print(response.json()[sys.argv[1]]['openssl_name']) #Prints out the translated cipher
