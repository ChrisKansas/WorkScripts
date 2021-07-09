#!/bin/bash

#Script to quickly format logs

#Check for arguments
if [ $# -eq 0 ]
then
  echo "[!] Usage: ./log-format.sh [LOG_FILE] [CSV_OUTPUT_FILE]" ; exit 1
fi

#Create Headers for the Output File
echo "Source IP,Time/Date,Method,Hostname,URI,Response Status,Response Size,Response Time,User-Agent,SSL Protocol,SSL Ciphers,Port,Origin IP" >> $2

while IFS= read -r LINE
  do
    # IPs
    IP=$(echo $LINE | cut -d " " -f 1)","
    echo -n $IP >> $2

    # timestamp
    TIMESTAMP=$(echo $LINE | cut -d " " -f 4 | cut -d "[" -f 2)","
    echo -n $TIMESTAMP >> $2

    #method
    METHOD=$(echo $LINE | cut -d " " -f 6 | cut -d '"' -f 2)","
    echo -n $METHOD >> $2

    #hostname
    HOSTNAME=$(echo $LINE | cut -d '"' -f 4 | cut -d ':' -f1)","
    echo -n $HOSTNAME >> $2

    #uri
    URI=$(echo $LINE | cut -d " " -f 7 | sed 's/,/;/g')","
    echo -n $URI >> $2

    #response status
    STATUS=$(echo $LINE | cut -d " " -f 9)","
    echo -n $STATUS >> $2

    #response size
    SIZE=$(echo $LINE | cut -d " " -f 10)","
    echo -n $SIZE >> $2

    #response time
    TIME=$(echo $LINE | cut -d '"' -f 18)","
    echo -n $TIME >> $2

    #UA
    UA=$(echo $LINE | cut -d '"' -f 6 | sed 's/,/;/g')","
    echo -n $UA >> $2

    #ssl_protocol
    PROTOCOL=$(echo $LINE | cut -d '"' -f 12)","
    echo -n $PROTOCOL >> $2

    #ssl_ciphers
    CIPHERS=$(echo $LINE | cut -d '"' -f 14)","
    echo -n $CIPHERS >> $2

    #port
    PORT=$(echo $LINE | cut -d '"' -f 16 | cut -d ":" -f2)","
    echo -n $PORT >> $2

    #origin IP
    OG_IP=$(echo $LINE | cut -d '"' -f 16 | cut -d ":" -f1)
    echo -n $OG_IP >> $2
    echo "" >> $2
  done < $1
