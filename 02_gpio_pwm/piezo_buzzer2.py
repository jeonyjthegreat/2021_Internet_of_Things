import RPi.GPIO as GPIO
import time
pin=12
GPIO.setmode(GPIO.BCM)
GPIO.setup(pin, GPIO.OUT)
pwm=GPIO.PWM(pin,1)
melody=[262,294,330,349,392,440,494,523]
pwm.start(50)
note = [4,4,5,5,4,4,2,4,4,2,2,1,4,4,5,5,4,4,2,4,2,1,2,0]
for i in note:
    pwm.ChangeFrequency(melody[i])
    time.sleep(0.3)
pwm.ChangeDutyCycle(0)
pwm.stop()
GPIO.cleanup()