#!/usr/bin/python
# Final proejct #

import threading
import RPi.GPIO as GPIO
import time
import urllib3
import Adafruit_DHT
import board
import json

from datetime import date, timedelta, datetime

GPIO.setwarnings(False) #disbaling warnings for some reason
GPIO.setmode(GPIO.BCM)



def getCurDate():
    today = date.today()
    return today.strftime("%Y-%m-%d")

def getYesterDate():
    return datetime.strftime(datetime.now()-timedelta(1), '%Y-%m-%d')
def queryHumidity():
    appkeyy = 'acac78e2-860f-4194-b27c-ebc296745833'
    curDatee = getCurDate()
    print("It is ",curDatee, " today")
    curDatee = getYesterDate()

    urll = 'http://et.water.ca.gov/api/data?appKey='
    targett = '&targets=75&startDate='
    dateStringg= '&endDate='
    queryString = urll + appkeyy + targett + curDatee + dateStringg + curDatee
    print("Querying to ", queryString)
        
    http = urllib3.PoolManager()
    resp = http.request('GET', queryString)
    data = resp.data
    values = json.loads(data)
    records = values['Data']['Providers'][0]['Records']
    print(records)
    humidity = records[0]["DayRelHumAvg"]["Value"]
    print("Humidity is", float(humidity))
    return float(humidity)


DHT_SENSOR = Adafruit_DHT.DHT11
DHT_PIN = 4
humidity = queryHumidity()

while True:

    humidity1, temperature1 = Adafruit_DHT.read(DHT_SENSOR,DHT_PIN)
    if temperature1 is None or humidity1 is None:
        print("error1")
    #read input
    time.sleep(1)

    humidity2, temperature2 = Adafruit_DHT.read(DHT_SENSOR,DHT_PIN)
    if temperature1 is None or humidity1 is None:
        print("error2")
    #read input
    time.sleep(1)

    humidity3, temperature3 = Adafruit_DHT.read(DHT_SENSOR,DHT_PIN)
    if temperature1 is None or humidity1 is None:
        print("error3")
    #read input
    time.sleep(1)
    #average measurements and feed to lcd
    
    temperature = (temperature1+temperature2+temperature3)/3.0
    print("Temp ", temperature)
    
        






