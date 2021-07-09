#!/bin/bash

FILE=$1

while IFS= read -r LINE
do
  grep $LINE $2
done < $FILE
