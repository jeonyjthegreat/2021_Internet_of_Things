import RPi.GPIO as GPIO
import time
pin=12
GPIO.setmode(GPIO.BCM)
GPIO.setup(pin, GPIO.OUT)
pwm=GPIO.PWM(pin,262)
pwm.start(50)
time.sleep(20)
pwm.ChangeDutyCycle(0)
pwm.stop()
GPIO.cleanup()