#!/usr/bin/python
import RPi.GPIO as GPIO
from time import sleep
from subprocess import check_output, Popen
from os import system

# Import all the other python scripts
import host
import ethernet
import cpu
import connection

pin1 = 24
pin2 = 23
pin3 = 4
pin4 = 17
pin5 = 22
pin6 = 27
pin7 = 18

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(pin1,GPIO.OUT)
GPIO.setup(pin2,GPIO.OUT)
GPIO.setup(pin3,GPIO.OUT)
GPIO.setup(pin4,GPIO.OUT)
GPIO.setup(pin5,GPIO.OUT)
GPIO.setup(pin6,GPIO.OUT)
GPIO.setup(pin7,GPIO.OUT)

x = 7
stime = 0.05

while not 'hostapd' in check_output(['ps','-A']):

  try:
    if x==7:
      wpin1 = pin1
      wpin2 = pin2
    elif x==6:
      wpin1 = pin2
      wpin2 = pin3
    elif x==5:
      wpin1 = pin3
      wpin2 = pin4
    elif x==4:
      wpin1 = pin4
      wpin2 = pin5
    elif x==3:
      wpin1 = pin5
      wpin2 = pin6
    elif x==2:
      wpin1 = pin6
      wpin2 = pin7
    elif x==1:
      x=8
      wpin1 = pin7
      wpin2 = pin1

    GPIO.output(wpin1,GPIO.LOW)
    sleep(stime)
    GPIO.output(wpin2,GPIO.HIGH)
    sleep(stime)
    x = x - 1
  except:
    break

GPIO.output(pin1,GPIO.HIGH)
GPIO.output(wpin1,GPIO.LOW)
GPIO.output(wpin2,GPIO.LOW)

Popen('sudo python /home/pi/led/connection.py',shell=True)
Popen('sudo python /home/pi/led/ethernet.py',shell=True)
Popen('sudo python /home/pi/led/cpu.py',shell=True)
Popen('sudo python /home/pi/led/host.py',shell=True)

system("sudo apt-get update")
update = system("sudo apt-get dist-upgrade -s |grep -P '^\d+ upgraded'|cut -d" " -f1").read()

if (update != '0'):
  GPIO.output(pin3,GPIO.HIGH)
