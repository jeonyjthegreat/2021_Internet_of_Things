import RPi.GPIO as GPIO
import time
pin=12
GPIO.setmode(GPIO.BCM)
GPIO.setup(pin, GPIO.OUT)
pwm=GPIO.PWM(pin, 50)
pwm.start(0)
try:
    while True:
        for i in range(0, 101, 1):
            pwm.ChangeDutyCycle(i)
            time.sleep(0.1)
        for i in range(100, -1, -1):
            pwm.ChangeDutyCycle(i)
            time.sleep(0.1)
finally:
    pwm.stop()
    GPIO.cleanup()