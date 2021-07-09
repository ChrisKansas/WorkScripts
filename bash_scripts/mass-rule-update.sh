#!/bin/bash

#Script to update multiple customer's rulesets

#Check for arguments
if [ $# -eq 0 ]
then
  echo "[!] Usage: ./mass-rule-update.sh [API_KEY] [RULE_TYPE] [CUSTOMER_LIST]" ; exit 1
fi

while IFS= read -r LINE
  do
    echo "Updating $LINE $2 rules now!"
    pipenv run python update-rules.py --api_key $1 --customer $LINE --rule_type $2 --rules_file ~/repos/WafRules/$2/$LINE.json
  done < $3
