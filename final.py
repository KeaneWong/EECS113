#!/usr/bin/python
# Final proejct #

import threading
import RPi.GPIO as GPIO
import time
import urllib3
import Adafruit_DHT
import json

from datetime import date, timedelta, datetime

###initialize board
GPIO.setwarnings(False) #disabling warnings for some reason
GPIO.setmode(GPIO.BCM)
###


###initialize DHT sensor
DHT_SENSOR = Adafruit_DHT.DHT11
DHT_PIN = 4
###

###initialize buttons
buttonDown = 25
buttonUp = 18
GPIO.setup(buttonDown, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(buttonUp, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.add_event_detect(buttonDown,GPIO.RISING)
GPIO.add_event_detect(buttonUp,GPIO.RISING)
###



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


humidity = queryHumidity()
targetTemperature = None

#detect buttons 3 times per second
def SenseButtons():
    if GPIO.event_detected(buttonUp):
        print("Button Up detected")
        targetTemperature = targetTemperature + 1.0
    if GPIO.event_detected(buttonDown):
        print("Button Down detected")
        targetTemperature = targetTemperature - 1.0
    sleep(0.33)

    if GPIO.event_detected(buttonUp):
        print("Button Up detected")
        targetTemperature = targetTemperature + 1.0
    if GPIO.event_detected(buttonDown):
        print("Button Down detected")
        targetTemperature = targetTemperature - 1.0
    sleep(0.33)

    if GPIO.event_detected(buttonUp):
        print("Button Up detected")
        targetTemperature = targetTemperature + 1.0
    if GPIO.event_detected(buttonDown):
        print("Button Down detected")
        targetTemperature = targetTemperature - 1.0
    sleep(0.33)


def HandleAC(doorsOpen, isHeating, isAC, targetTemperature, trueTemp, energyUsed):
    if not doorsOpen:
        if targetTemperature - trueTemp  > 3.0 and not isHeating: #implies current temperature is too low and heater must be turned on
            ###function to print "Heater is On" to LCD. Hold for 3 seconds
            print("Turn on Heater")
            isHeating = True
            ###function to report energy bill to LCD
        elif targetTemperature - trueTemp < -3.0 and not isAC: #implies current temperature is too high and ac must be turned on
            ###function to print "AC Is On" to LCD. Hold for 3 seconds
            print("Turn on AC")
            isAC = True
            ###function to report energy bill to LCD
        elif isAC:
            ###function to print "Ac is off" to lcd. Hold for 3 seconds
            print("AC turned off")
            isAC = False
            ###function to report energy bill to LCD
        elif isHeating:
            ###function to print "Heating is Off". Hold for 3 seconds
            print("Heating turned off")
            isHeating = False
            ###function to report energy bill to LCD
    else:
        if isAC:
            ###function to print "AC is Off, Windows open". Hold for 3 seconds
            print("Turn Off AC; Windows open")
            isAC = False
            ###function to report energy bill to LCD
        if isHeating:
            ###function to print "Heating is Off, Windows open". Hold for 3 seconds
            print("Turn off heating; Windows open")
            isHeating = False
            ###function to report energy bill to LCD
    return isHeating, isAC

def SenseTemperature():
    doorsOpen = False
    isHeating = False
    isAC = False

    hum0, targetTemperature = Adafruit_DHT.read(DHT_SENSOR,DHT_PIN) #initialize targetTemperature before first SenseButtons call
    targetTemperature = targetTemperature + 0.05*humidity

    energyUsed = 0.0
    while True:

        humidity1, temperature1 = Adafruit_DHT.read(DHT_SENSOR,DHT_PIN)
        if temperature1 is None or humidity1 is None:
            print("error1")

        #read input
        SenseButtons()
        
        humidity2, temperature2 = Adafruit_DHT.read(DHT_SENSOR,DHT_PIN)
        if temperature1 is None or humidity1 is None:
            print("error2")

        #read input
        SenseButtons()
        
        humidity3, temperature3 = Adafruit_DHT.read(DHT_SENSOR,DHT_PIN)
        if temperature1 is None or humidity1 is None:
            print("error3")

        #read input
        SenseButtons()

        #average measurements and feed to lcd
        temperature = (temperature1+temperature2+temperature3)/3.0
        print("Temperature is ", temperature)

        trueTemp = temperature + 0.05 * humidity

        if isAC: ###add watts
            energyUsed = energyUsed + 54000.0
        elif isHeating:
            energyUsed = energyUsed + 108000.0 

        isHeating, isAC = HandleAC(doorsOpen,isHeating,isAC, targetTemperature, trueTemp, energyUsed)



SenseTemperature()









