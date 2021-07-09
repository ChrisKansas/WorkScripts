#/bin/bash
#Curl to rotate IPs

for i in {1..9}
do
  curl -s -D - -o /dev/null -b cookie.txt -c cookie.txt -H "X-Forwarded-For: 1.212.31.18$i" http://soclab1-dvwa.securedmz.com/login.php  
done
