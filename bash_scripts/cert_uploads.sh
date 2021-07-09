#!/bin/bash

#Handles uploaded certs

if [ -z "$1" ]
then
	echo "Please provide the cert name."
else
	CERT=$1
  	CERTPATH=/opt/threatx/Public_Site/uploads/$CERT
  	ssh ch05-prod "docker exec upload-5 /bin/bash -c 'cat $CERTPATH'" &>/dev/null
	if [ $? -eq 0 ]; 
	then 
		echo "----CERT DATES----"
		ssh ch05-prod "docker exec upload-5 /bin/bash -c 'cat $CERTPATH'"  | openssl x509 -noout -dates
		echo "----SITE NAMES----" 	
		ssh ch05-prod "docker exec upload-5 /bin/bash -c 'cat $CERTPATH'" | openssl x509 -noout -text | grep -i dns
		echo "----KEY/CERT CHECK----"
		if [[ $(diff <(ssh ch05-prod "docker exec upload-5 /bin/bash -c 'cat $CERTPATH'" | openssl x509 -noout -modulus | openssl md5) <(ssh ch05-prod "docker exec upload-5 /bin/bash -c 'cat $CERTPATH'" | openssl rsa -noout -modulus| openssl md5)) ]];
		then
			echo "The Key does not match the cert. Let the customer know."; exit 1
		else
			echo "The Key matches the cert! Good to go!"
		fi
  		echo "----CERT CHAIN----"
		ssh ch05-prod "docker exec upload-5 /bin/bash -c 'cat $CERTPATH'"
		echo "----REMOVING CERT----"
		ssh ch05-prod "docker exec upload-5 /bin/bash -c 'rm $CERTPATH'"
		echo "Cert has been removed."
	else
		echo "Please check the cert exists or the name is correct." ; exit 1
	fi
fi
