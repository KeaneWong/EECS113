#!/usr/bin/python
# Final proejct #

import threading
import RPi.GPIO as GPIO
import time
import Adafruit_DHT
import board
from datetime import date

GPIO.setwarnings(False) #disbaling warnings for some reason
GPIO.setmode(GPIO.BCM)



def getCurDate():
    today = date.today()
    return today.strftime("%Y-%m-%d")


appkey = 'acac78e2-860f-4194-b27c-ebc296745833'
curDate = getCurDate()
print("It is ",curDate, " today")

DHT_SENSOR = Adafruit_DHT.DHT11
DHT_PIN = 4
while True:

    #temperature1 = dht_device.temperature
    #humidity1 = dht_device.humidity
    humidity1, temperature1 = Adafruit_DHT.read(DHT_SENSOR,DHT_PIN)
    if temperature1 is None or humidity1 is None:
        print("error")
    #read input
    time.sleep(1)

    humidity2, temperature2 = Adafruit_DHT.read(DHT_SENSOR,DHT_PIN)
    #read input
    time.sleep(1)

    humidity3, temperature3 = Adafruit_DHT.read(DHT_SENSOR,DHT_PIN)
    #read input
    time.sleep(1)
    #average measurements and feed to lcd
    
    temperature = (temperature1+temperature2+temperature3)/3.0
    print("Temp ", temperature)
    
        






