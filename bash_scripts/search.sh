#!/bin/bash

#Script to search for stuff

#Check for arguments
if [ $# -eq 0 ]
then
  echo "[!] Usage: ./search.sh [SEARCH_FILE] [WHAT_TO_SEARCH]" ; exit 1
fi

while IFS= read -r LINE
  do
    if [[ $(grep "$LINE" $2) ]];
    then
      echo "$LINE"
    else
      :
    fi
  done < $1
