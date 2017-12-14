#!/usr/bin/python
import RPi.GPIO as GPIO
from time import sleep
from psutil import cpu_percent

pin = 23

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(pin,GPIO.OUT)

while True:

  CPU = cpu_percent()

  if CPU > 15:
    #GPIO.output(pin,GPIO.LOW)
    #sleep(0.3)
    GPIO.output(pin,GPIO.HIGH)
  else:
    GPIO.output(pin,GPIO.LOW)

  sleep(0.5)
