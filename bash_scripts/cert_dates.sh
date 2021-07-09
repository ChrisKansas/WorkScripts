#!/bin/bash
if [[ $1 == "-f" ]]
then
  FILE=$2
  while IFS= read -r LINE
  do
    echo "---------------"
    echo $LINE
    echo | openssl s_client -servername $LINE -connect $LINE:443 2>/dev/null | openssl x509 -noout -dates
  done < $FILE
else
  SITE=$1
  echo | openssl s_client -servername $SITE -connect $SITE:443 2>/dev/null | openssl x509 -noout -dates
fi

