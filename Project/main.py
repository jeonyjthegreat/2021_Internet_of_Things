import RPi.GPIO as GPIO
import picamera
import time
led=4
btn=5
GPIO.setmode(GPIO.BCM)
GPIO.setup(led, GPIO.OUT)
#GPIO.setup(btn, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(btn, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
camera=picamera.PiCamera()
path = '/home/pi/src/Project'
try:
    camera.resolution=(640, 480)
    camera.start_preview()
    time.sleep(2)
    camera.rotation=180
    while True:
        val=GPIO.input(btn)
        if val==1:
            camera.capture('%s/photo.jpg' % path)
        GPIO.output(led, val)
        time.sleep(0.1)
        
finally:
    GPIO.cleanup()