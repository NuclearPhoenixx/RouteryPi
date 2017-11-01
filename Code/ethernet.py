import RPi.GPIO as GPIO
from time import sleep
import subprocess

pin = 27

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(pin,GPIO.OUT)

while True:
  eth = subprocess.check_output('cat /sys/class/net/eth0/operstate', shell=True)
  if 'up' in eth:
    GPIO.output(pin,GPIO.HIGH)
  else:
    GPIO.output(pin,GPIO.LOW)

  sleep(2)
