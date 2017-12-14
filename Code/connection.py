#!/usr/bin/python
#import RPi.GPIO as GPIO
#from time import sleep
#from os import system

pin = 22

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(pin,GPIO.OUT)

def connection():

  response = system("ping -c 1 8.8.8.8 ")

  if response == 0:
    return True
  else:
    return False

def connectionFunction():
  
  if connection():
    GPIO.output(pin,GPIO.HIGH)
  else:
    GPIO.output(pin,GPIO.LOW)

  sleep(4)
