import RPi.GPIO as GPIO
LED_PIN=4
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)
try:
	while True:
		val=input("1:on, 0:off, 9:exit >")
		if val=='0':
			GPIO.output(LED_PIN,GPIO.LOW)
			print("LED off")
		elif val=='1':
			GPIO.output(LED_PIN,GPIO.HIGH)
			print("LED on")
		elif val=='9':
			GPIO.output(LED_PIN,GPIO.LOW)
			break
finally:
	GPIO.cleanup()
	print("cleanup and exit")
