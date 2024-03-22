#! /usr/bin/env python
# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO
import time
import sys
import requests

GPIO_BUTTON = 16
DELAY_TIME = 1

# Set the GPIO pin mode
GPIO.setmode(GPIO.BCM)
GPIO.setup(GPIO_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Function to send data via HTTP
def send_data(state):
    cmd = ('http://cobra:18011982fx@192.168.0.3:8080/json.htm?type=command&param=udevice&idx=248&nvalue=' + str(state))
    try:
        requests.get(cmd)
    except:
        print("Sending to telegram...")
    if state == 0:
        cmd2 = "https://api.telegram.org/bot1060079381:AAHlZvRxFpqeRIqp1nJBUexXScRpJWdBiWs/sendMessage?chat_id=-1001493931760&text=Пропало живлення будинку!"
        cmd3 = "https://api.telegram.org/bot1060079381:AAHlZvRxFpqeRIqp1nJBUexXScRpJWdBiWs/sendMessage?chat_id=-1001244728283&text=Пропало живлення будинку!"
    else:
        cmd2 = "https://api.telegram.org/bot1060079381:AAHlZvRxFpqeRIqp1nJBUexXScRpJWdBiWs/sendMessage?chat_id=-1001493931760&text=Відновилось живлення будинку!"
	cmd3 = "https://api.telegram.org/bot1060079381:AAHlZvRxFpqeRIqp1nJBUexXScRpJWdBiWs/sendMessage?chat_id=-1001244728283&text=Відновилось живлення будинку!"
    try:
        requests.get(cmd2)
        requests.get(cmd3)
    except:
        print("Was sended to telegram")

# Get and print the initial state of the GPIO pin
initial_state = GPIO.input(GPIO_BUTTON)
if initial_state == GPIO.HIGH:
    print("Initial state of GPIO 16: HIGH")
    send_data(0)
else:
    print("Initial state of GPIO 16: LOW")
    send_data(1)

# Initialize a variable to store the previous state
previous_state = initial_state

while True:
    time.sleep(DELAY_TIME)
    # Get the current state of the GPIO pin
    input_state = GPIO.input(GPIO_BUTTON)
    # Compare the current state with the previous state
    if input_state != previous_state:
        if input_state == GPIO.HIGH:
            print("GPIO 16: HIGH")
            send_data(0)
        else:
            print("GPIO 16: LOW")
            send_data(1)
        # Update the previous state
        previous_state = input_state

# Clean up the GPIO pins
GPIO.cleanup()
