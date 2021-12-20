import RPi.GPIO as GPIO

BUTTON_PIN1 = 5
LED_PIN1 = 16
BUTTON_PIN2 = 6
LED_PIN2 = 20

GPIO.setmode(GPIO.BCM)

GPIO.setup(LED_PIN1, GPIO.OUT)
GPIO.setup(LED_PIN2, GPIO.OUT)
GPIO.setup(BUTTON_PIN1, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(BUTTON_PIN2, GPIO.IN, pull_up_down = GPIO.PUD_UP)
try:
    while True:
        if GPIO.input(BUTTON_PIN1)==1:
            GPIO.output(LED_PIN1, GPIO.input(BUTTON_PIN1))
        if GPIO.input(BUTTON_PIN2)==1:
            GPIO.output(LED_PIN2, GPIO.input(BUTTON_PIN2))
        
finally:
    GPIO.cleanup()
    print('cleanup and exit')