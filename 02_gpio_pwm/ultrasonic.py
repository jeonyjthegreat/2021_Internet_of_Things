from _typeshed import StrPath
import RPi.GPIO as GPIO
import time
tp=4
ep=5
GPIO.setmode(GPIO.BCM)
GPIO.setup(tp, GPIO.OUT)
GPIO.setup(ep, GPIO.IN)
try:
    while True:
        GPIO.output(tp, GPIO.HIGH)
        time.sleep(0.00001)
        GPIO.output(tp, GPIO.LOW)
        while GPIO.input(ep)==0: 
            pass
        start=time.time()
        print(start)
        while GPIO.input(ep)==1: 
            pass
        stop=time.time()
        print(stop)
        dt=stop-start
        dist=17160*dt
        print('Distance : %.1fcm' % dist)
        time.sleep(0.1)
finally: