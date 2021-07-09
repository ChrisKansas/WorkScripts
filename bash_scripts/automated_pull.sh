#!/bin/bash

# Get our date and hour
DATE=$(date +'%Y%m%d')
HOUR=$(date +'%H')

# Check if Monday; pull logs
if [[ $(date '+%a') == 'Mon' && ${HOUR#0} -lt 12 ]]; then
  echo "Fetching BMC weekend logs!"
  echo ""
  customer-fetch-log bmc access.log.2.gz
  customer-fetch-log bmc access.log.1
  customer-fetch-log bmc access.log
else
  echo "Fetching BMC access log!"
  echo ""
  customer-fetch-log bmc access.log
fi

# Change dir to log location
cd /opt/logmart/logs/bmc/"$DATE"

echo ""

# Check for 504s
echo "Checking for 504 connection timeouts!"
echo ""

# Command to check for Connection Timeouts
grep "customerapps.bmc\|documents.bmc\|efix.bmc\|spac.bmc\|veb.bmc\|webapps.bmc\|webepd.bmc\|zsojira\|mybidev.bmc\|mybiqa.bmc\|mybi.bmc\|egw.bmc\|webapi.bmc\|tableau.bmc" * | awk '{ if ($9 == 504 && $(NF-1) ~ /60\./) print $0}' | cut -d ":" -f2- >> $HOME/timeouts.txt

# Check if Timeouts Exist
if [[ -s $HOME/timeouts.txt ]]; then
  cat $HOME/timeouts.txt
else
  echo "There were no connection timeouts!"
fi

echo ""
