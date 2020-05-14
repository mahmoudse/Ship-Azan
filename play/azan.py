#! /usr/bin/env python
import RPi.GPIO as GPIO
import os, sys
import time


GPIO.setmode(GPIO.BCM) # GPIO Numbers instead of board numbers
RELAIS_1_GPIO = 12
GPIO.setup(RELAIS_1_GPIO, GPIO.OUT) # GPIO Assign mode


print("Start")
time.sleep(3) # Sleep for 3 seconds
print("Delay")

GPIO.output(RELAIS_1_GPIO, GPIO.LOW) # out
os.system('omxplayer -o local /home/pi/Desktop/file.mp3 > /dev/null 2>&1')
print("End")
GPIO.output(RELAIS_1_GPIO, GPIO.HIGH) # on


GPIO.cleanup() # cleanup all GPIO 
sys.exit()
