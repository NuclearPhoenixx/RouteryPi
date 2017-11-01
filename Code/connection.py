import RPi.GPIO as GPIO
from time import sleep
import os

pin = 22

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(pin,GPIO.OUT)

def connection():
  response = os.system("ping -c 1 8.8.8.8 ")
  if response == 0:
    return True
  else:
    return False

while True:
  if connection():
    GPIO.output(pin,GPIO.HIGH)
  else:
    GPIO.output(pin,GPIO.LOW)
  sleep(4)
