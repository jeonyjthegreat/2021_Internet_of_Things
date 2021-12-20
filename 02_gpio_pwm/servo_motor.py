import RPi.GPIO as GPIO
sp=4
GPIO.setmode(GPIO.BCM)
GPIO.setup(sp, GPIO.OUT)
pwm=GPIO.PWM(sp, 50)
pwm.start(7.5)
try:
    while True:
        val= input('1: 0도, 2: -90도, 3: 90도, 9:Exit')
        if val=='1':
            pwm.ChangeDutyCycle(7.5)
        elif val=='2':
            pwm.ChangeDutyCycle(25)
        elif val=='3':
            pwm.ChangeDutyCycle(12.5)
        elif val=='9':
            break
finally:
    pwm.stop()
    GPIO.cleanup()