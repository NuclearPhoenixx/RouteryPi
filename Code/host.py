#!/usr/bin/python
import RPi.GPIO as GPIO
from time import sleep
from subprocess import check_output

pin = 24

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(pin,GPIO.OUT)

while True:

  if 'hostapd' in check_output(['ps','-A']):
    GPIO.output(pin,GPIO.HIGH)
  else:
    GPIO.output(pin,GPIO.LOW)

  sleep(4)
