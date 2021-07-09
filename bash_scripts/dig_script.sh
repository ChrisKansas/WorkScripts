#!/bin/bash

FILE=$1

while IFS= read -r LINE
  do
    echo | dig $LINE
  done < $FILE

