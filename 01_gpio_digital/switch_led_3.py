import RPi.GPIO as GPIO
ys=11
y=14
r=13
rs=10
g=15
gs=12
GPIO.setmode(GPIO.BCM)
GPIO.setup(r, GPIO.OUT)
GPIO.setup(y, GPIO.OUT)
GPIO.setup(g, GPIO.OUT)
GPIO.setup(ys, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(rs, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(gs, GPIO.IN, pull_up_down = GPIO.PUD_UP)
try:
    while True:
        GPIO.output(r, GPIO.input(rs)-1)
        GPIO.output(y, GPIO.input(ys)-1)
        GPIO.output(g, GPIO.input(gs)-1)
finally:
    GPIO.cleanup()
    print('cleanup and exit')