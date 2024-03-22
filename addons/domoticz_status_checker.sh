#!/bin/sh
#status=`curl -m 60 -s -i -H "Accept: application/json" "http://127.0.0.1:8080/json.htm?type=devices&rid=1" | grep "status"| awk -F: '{print $2}'|sed 's/,//'| sed 's/\"//g'`
status=`curl -m 60 -s -i -H "Accept: application/json" "http://127.0.0.1:8080/json.htm?type=command&param=getversion" | grep "status"| awk -F : '{print $2}' | sed 's/,//' | sed 's/\"//g'`
if [ $status ]
then
echo "Domoticz працює. Нічого робити не потрібно..."
else
echo 'Domoticz не працює. Перезавантажую Domoticz...'
/usr/bin/curl -s "https://api.telegram.org/bot1060079381:AAHlZvRxFpqeRIqp1nJBUexXScRpJWdBiWs/sendMessage?chat_id=-1001244728283&text=Систему Domoticz перезапущено!" > /dev/null
systemctl restart docker-compose-app
fi
