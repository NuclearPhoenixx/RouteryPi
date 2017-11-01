import RPi.GPIO as GPIO
from time import sleep
import subprocess

pin = 24

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(pin,GPIO.OUT)

while True:
  if 'hostapd' in subprocess.check_output(['ps','-A']):
    GPIO.output(pin,GPIO.HIGH)
  else:
    GPIO.output(pin,GPIO.LOW)
  sleep(4)
