import RPi.GPIO as GPIO
import time
SEGMENT_PINS=[2,3,4,5,6,7,8]
DIGIT_PINS=[10,11,12,13]
GPIO.setmode(GPIO.BCM)
for segment in SEGMENT_PINS:
    GPIO.setup(segment, GPIO.OUT)
    GPIO.output(segment, GPIO.LOW)
for digit in DIGIT_PINS: #HIGH > OFF, LOW > ON
    GPIO.setup(segment, GPIO.OUT)
    GPIO.output(segment, GPIO.HIGH)
data = [[1, 1, 1, 1, 1, 1, 0],  # 0
        [0, 1, 1, 0, 0, 0, 0],  # 1
        [1, 1, 0, 1, 1, 0, 1],  # 2
        [1, 1, 1, 1, 0, 0, 1],  # 3
        [0, 1, 1, 0, 0, 1, 1],  # 4
        [1, 0, 1, 1, 0, 1, 1],  # 5
        [1, 0, 1, 1, 1, 1, 1],  # 6
        [1, 1, 1, 0, 0, 0, 0],  # 7
        [1, 1, 1, 1, 1, 1, 1],  # 8
        [1, 1, 1, 0, 0, 1, 1]]  # 9
note = [4,4,5,5,4,4,2,4,4,2,2,1,4,4,5,5,4,4,2,4,2,1,2,0]
def display(digit, number):
    for i in range(4):
        if i+1==digit :
            GPIO.output(DIGIT_PINS[i], GPIO.LOW)
        else :
            GPIO.output(DIGIT_PINS[i], GPIO.HIGH)
    for i in range(7):
        GPIO.putput(SEGMENT_PINS[i], data[number][i])
    time.sleep(0.001)
try:
    while True:
        display(1,2)
        display(2,0)
        display(3,2)
        display(4,1)
finally:
    GPIO.cleanup()
    print('by')