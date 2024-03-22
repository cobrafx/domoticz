#!/usr/bin/python3

from pymodbus.client.sync import ModbusTcpClient
from pymodbus.payload import BinaryPayloadDecoder
from pymodbus.constants import Endian

import time
import os
import sys
import datetime
import requests

from datetime import datetime

while True:


  now = datetime.now()

  if( int(now.strftime("%H")) >= 5 and  int(now.strftime("%H")) <= 23 ):

    time.sleep(10)
    try:


      # Встановлюємо з'єднання з сервером Modbus TCP
      client = ModbusTcpClient('192.168.0.44', port=502)
      client.connect()

      # Змінюємо ідентифікатор slave на 1
      client.unit_id = 1

      # Задаємо адресу регістру та кількість регістрів для зчитування
      address = 32080
      quantity = 2

      # Зчитуємо значення зареєстрованих регістрів
      result = client.read_holding_registers(address=address, count=quantity, unit=1)
      if result.isError():
          print(f"Помилка: {result}")
      else:
          # Розпаковуємо значення регістрів з бінарного формату та конвертуємо до знакового цілого типу
          decoder = BinaryPayloadDecoder.fromRegisters(result.registers, byteorder=Endian.Big, wordorder=Endian.Big)
          active_power = decoder.decode_32bit_int()
          if (active_power is not None):
             print('active_power = '+ str(active_power))
             cmd = ('http://cobra:18011982fx@192.168.0.3:8080/json.htm?type=command&param=udevice&idx=194&nvalue=0&svalue=' + str(active_power))
             try:
               requests.get(cmd)
             except:
               print("Send")
          else:
             print('Failed to get reading. Try again!')




      # Задаємо адресу регістру та кількість регістрів для зчитування
      address2 = 32114
      quantity2 = 2

      # Зчитуємо значення зареєстрованих регістрів
      result2 = client.read_holding_registers(address=address2, count=quantity2, unit=1)
      if result2.isError():
          print(f"Помилка: {result}")
      else:
          # Розпаковуємо значення регістрів з бінарного формату та конвертуємо до знакового цілого типу
          decoder = BinaryPayloadDecoder.fromRegisters(result2.registers, byteorder=Endian.Big, wordorder=Endian.Big)
          daily_power = decoder.decode_32bit_int() * 10
          if (daily_power is not None):
             print('daily_power = '+ str(daily_power))
             cmd = ('http://cobra:18011982fx@192.168.0.3:8080/json.htm?type=command&param=udevice&idx=195&nvalue=0&svalue=' + str(daily_power))
             try:
               requests.get(cmd)
             except:
               print("Send")
          else:
             print('Failed to get reading. Try again!')


      addressA = 32069
      quantityA = 1

      # Зчитуємо значення зареєстрованих регістрів
      result = client.read_holding_registers(address=addressA, count=quantityA, unit=1)
      if result.isError():
          print(f"Помилка: {result}")
      else:
          # Розпаковуємо значення регістрів з бінарного формату та конвертуємо до знакового цілого типу
          decoder = BinaryPayloadDecoder.fromRegisters(result.registers, byteorder=Endian.Big, wordorder=Endian.Big)
          Ua = decoder.decode_16bit_int() / 10
          if (Ua is not None):
             print('Ua = '+ str(Ua))
             cmd = ('http://cobra:18011982fx@192.168.0.3:8080/json.htm?type=command&param=udevice&idx=262&nvalue=0&svalue=' + str(Ua))
             try:
               requests.get(cmd)
             except:
               print("Send")
          else:
             print('Failed to get reading. Try again!')


      addressB = 32070
      quantityB = 1

      # Зчитуємо значення зареєстрованих регістрів
      result = client.read_holding_registers(address=addressB, count=quantityB, unit=1)
      if result.isError():
          print(f"Помилка: {result}")
      else:
          # Розпаковуємо значення регістрів з бінарного формату та конвертуємо до знакового цілого типу
          decoder = BinaryPayloadDecoder.fromRegisters(result.registers, byteorder=Endian.Big, wordorder=Endian.Big)
          Ub = decoder.decode_16bit_int() / 10
          if (Ub is not None):
             print('Ub = '+ str(Ub))
             cmd = ('http://cobra:18011982fx@192.168.0.3:8080/json.htm?type=command&param=udevice&idx=263&nvalue=0&svalue=' + str(Ub))
             try:
               requests.get(cmd)
             except:
               print("Send")
          else:
             print('Failed to get reading. Try again!')


      addressC = 32071
      quantityC = 1

      # Зчитуємо значення зареєстрованих регістрів
      result = client.read_holding_registers(address=addressC, count=quantityC, unit=1)
      if result.isError():
          print(f"Помилка: {result}")
      else:
          # Розпаковуємо значення регістрів з бінарного формату та конвертуємо до знакового цілого типу
          decoder = BinaryPayloadDecoder.fromRegisters(result.registers, byteorder=Endian.Big, wordorder=Endian.Big)
          Uc = decoder.decode_16bit_int() / 10
          if (Uc is not None):
             print('Ub = '+ str(Uc))
             cmd = ('http://cobra:18011982fx@192.168.0.3:8080/json.htm?type=command&param=udevice&idx=264&nvalue=0&svalue=' + str(Uc))
             try:
               requests.get(cmd)
             except:
               print("Send")
          else:
             print('Failed to get reading. Try again!')


      # Закриваємо з'єднання з сервером Modbus TCP
      client.close()

    except:
         cmd = ('http://cobra:18011982fx@192.168.0.3:8080/json.htm?type=command&param=udevice&idx=194&nvalue=0&svalue=0')
         requests.get(cmd)

