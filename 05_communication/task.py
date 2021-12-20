import spidev
import RPi.GPIO as GPIO
import time
pin=4
GPIO.setmode(GPIO.BCM)
GPIO.setup(pin, GPIO.OUT)
spi=spidev.SpiDev()
spi.open(0,0)
spi.max_speed_hz=100000
def analog_read(channel):
    ret=spi.xfer2([1,(8+channel)<<4,0])
    adc_out=((ret[1]&3)<<8)+ret[2]
    return adc_out
try:
    while True:
        ldr_value=analog_read(0)
        print("LDR-%d"%ldr_value)
        if(ldr_value<812):
            GPIO.output(pin, GPIO.HIGH)
        else:
            GPIO.output(pin, GPIO.LOW)
finally:
    spi.close()