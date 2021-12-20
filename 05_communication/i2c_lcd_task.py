import time
import Adafruit_DHT
import datetime
from lcd import drivers
display=drivers.Lcd()
sensor=Adafruit_DHT.DHT11
pin=4
try:
    print("Writing to display")
    
    while True:
        now=datetime.datetime.now()
        display.lcd_display_string(now.strftime("%x%X"),1)
        humidity, temperature=Adafruit_DHT.read_retry(sensor, pin)
        if humidity is not None and temperature is not None:
            string=str(temperature)+'*C, '+str(humidity)+'%'
            display.lcd_display_string(string,2)
            display.lcd_display_string(now.strftime("%x%X"),1)
        else:
            display.lcd_display_string(now.strftime("%x%X"),1)
            print('Read error')
        #time.sleep(0.1)
finally:
    print("End of program")
