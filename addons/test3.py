#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import serial, re
import requests, ast

serial = serial.Serial('/dev/ttyUSB0', 9600, timeout=1);

try:
  while True:
#    serial.write('hello');
    response = serial.readall();
    h = re.search(r'Влажность: (\d{2}\.\d{2})', response,  flags=re.LOCALE);
    t = re.search(r'Температура: (\d{2}\.\d{2})', response,  flags=re.LOCALE);

    print (response)

    if h is not None and t is not None:
       print (h.group(1));
       print (t.group(1));
       temperature = ast.literal_eval(t.group(1));
       humidity = ast.literal_eval(h.group(1));
       cmd = ('http://192.168.0.3:8080/json.htm?type=command&param=udevice&idx=204&nvalue=0&svalue=' +  '{0:0.1f}'.format(temperature) +  ';' +  '{0:0.0f}'.format(humidity) +  ';0');
    #   print(cmd);
       requests.get(cmd);
       break;
#    print response;
except:
  serial.close();
