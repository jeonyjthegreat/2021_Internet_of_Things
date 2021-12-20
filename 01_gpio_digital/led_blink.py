import RPi.GPIO as GPIO
import time

LED_PIN = 4
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)

for i in range(10):
    GPIO.output(LED_PIN, GPIO.HIGH)
    print("led on")
    time.sleep(1)

    GPIO.output(LED_PIN, GPIO.LOW)
    print("led off")
    time.sleep(1)

GPIO.cleanup()