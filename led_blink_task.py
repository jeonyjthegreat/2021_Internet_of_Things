import RPi.GPIO as GPIO
import time
def on(led):
  GPIO.setup(led, GPIO.OUT)
  GPIO.output(led, GPIO.HIGH)
  print("led on")
  time.sleep(2)

  GPIO.output(led, GPIO.LOW)
  print("led off")
  #time.sleep(2)

LED_PIN1=4
LED_PIN2=5
LED_PIN3=6
GPIO.setmode(GPIO.BCM)

on(LED_PIN1)
on(LED_PIN2)
on(LED_PIN3)

GPIO.cleanup()