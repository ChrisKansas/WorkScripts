#!/bin/bash
  FILE=$1
  while IFS= read -r LINE
  do
    whois -h whois.radb.net -- "-i origin ${LINE}" | grep -Eo "([0-9.]+){4}/[0-9]+"
  done < $FILE
