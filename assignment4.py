#!/usr/bin/python
# Assignment 4 #

import threading
import RPi.GPIO as GPIO
import time

###Pin numbering declaratin here

###Set GPIO pins for i/o and all setupts needed based on assignment pdf
period = 1
blinkingMode = False
curState = {22: True, 12: True, 13: True, 15: True}
#This function takes care of blinking an is called by blinking thread
blink_mode = False


GPIO.setwarnings(False) #disbaling warnings for some reason
GPIO.setmode(GPIO.BOARD)
greenButton = 22
redButton = 12
yellowButton = 13
blueButton = 15

greenLed = 29
redLed = 31
yellowLed = 32
blueLed = 33
GPIO.setup(greenButton, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(redButton, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(yellowButton, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(blueButton, GPIO.IN, pull_up_down = GPIO.PUD_UP)

GPIO.setup(greenLed, GPIO.OUT)
GPIO.setup(redLed, GPIO.OUT)
GPIO.setup(yellowLed, GPIO.OUT)
GPIO.setup(blueLed, GPIO.OUT)

GPIO.output(greenLed, True)
GPIO.output(redLed, True)
GPIO.output(yellowLed, True)
GPIO.output(blueLed, True)

GPIO.add_event_detect(greenButton,GPIO.RISING)
GPIO.add_event_detect(redButton,GPIO.RISING)
GPIO.add_event_detect(yellowButton,GPIO.RISING)
GPIO.add_event_detect(blueButton,GPIO.RISING)

#GPIO.add_event_detect(22,GPIO.FALLING, handleRev)
#GPIO.add_event_detect(12,GPIO.FALLING, handleRev)
#GPIO.add_event_detect(13,GPIO.FALLING, handleRev)
#GPIO.add_event_detect(15,GPIO.FALLING, handleRev)

blinkingMode = False
delay = 1.0
timer = 0.0
ledState = True


def ledActivate(ledon):
    GPIO.output(greenLed, ledon)
    GPIO.output(redLed, ledon)
    GPIO.output(yellowLed, ledon)
    GPIO.output(blueLed, ledon)
    #ledon = not ledon
    #print(ledon)

while True:
    if GPIO.event_detected(yellowButton) and GPIO.event_detected(blueButton):
        print(GPIO.input(yellowButton))
        blinkingMode = not blinkingMode
        timer = 0.0
        delay = 1.0
        if not blinkingMode:
            GPIO.output(greenLed,False)
            GPIO.output(redLed,False)
            GPIO.output(yellowLed,False)
            GPIO.output(blueLed,False)
    if blinkingMode :
        if GPIO.event_detected(greenButton):
            GPIO.output(redLed,False)
            delay = delay/2
        elif GPIO.event_detected(redButton):
            print('red')
            delay = delay*2
        ledActivate(ledState)
        ledState = not ledState
        time.sleep(delay/2.0)
        print(delay/2.0)
        timer = timer + delay/2.0
        if timer > 10:
            blinkingMode = fFalse
            GPIO,ouput(yellowLed,False)
            GPIO.output(blueLed,False)
            GPIO,ouput(redLed,False)
            GPIO,ouput(greenLed,False)
    if GPIO.event_detected(yellowButton) or GPIO.event_detected(blueButton) :
        print("Hello")
    time.sleep(1e8)
        
 
        





