import RPi.GPIO as GPIO
import time

SEGMENT_PINS=[2,3,4,5,6,7,8] #4digits를 사용하기 위한 핀 번호
dp=9 #decimal 핀 번호
buzzer=24 #부저 핀 번호
sumbtn=20 #시간을 설정해 주는 버튼 핀 번호
cdbtn=21 #시작 버튼 핀 번호
DIGIT_PINS=[10,11,12,13] #4digits D1, D2, D3, D4 핀 번호
flag=0 #정상적인 프로그램 종료를 위한 플래그
led=19 #led

GPIO.setmode(GPIO.BCM)
melody=[262,294,330,349,392,440,494,523]
note = [4,4,5,5,4,4,2,4,4,2,2,1,4,4,5,5,4,4,2,4,2,1,2,0] #악보
GPIO.setup(dp, GPIO.OUT)
GPIO.setup(led, GPIO.OUT)
GPIO.output(led,0)
GPIO.setup(buzzer, GPIO.OUT)
GPIO.setup(cdbtn, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(sumbtn, GPIO.IN, pull_up_down=GPIO.PUD_UP)
pwm=GPIO.PWM(buzzer,1)
GPIO.output(dp,1)
for segment in SEGMENT_PINS:
    GPIO.setup(segment, GPIO.OUT)
    GPIO.output(segment, GPIO.LOW)
for digit in DIGIT_PINS: #HIGH > OFF, LOW > ON
    GPIO.setup(digit, GPIO.OUT)
    GPIO.output(digit, GPIO.HIGH)
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
def dp(digit, number): #자릿수, 숫자
    for i in range(4):
        if i+1==digit :
            GPIO.output(DIGIT_PINS[i], GPIO.LOW)
        else :
            GPIO.output(DIGIT_PINS[i], GPIO.HIGH)
    for i in range(7):
        GPIO.output(SEGMENT_PINS[i], data[number][i])
    time.sleep(0.001)
def play():
    pwm.start(50)
    for i in note:
        pwm.ChangeFrequency(melody[i])
        time.sleep(0.3)
    pwm.ChangeDutyCycle(0)
    pwm.stop()
def display(x):
    #a=int(x/1000)
    #b=int(x%1000/100)
    #c=int(x%100/10)
    #d=int(x%10)
    d=x%10
    c=x%60/10
    b=x/60%10
    a=x/600
    dp(1, int(a))
    dp(2, int(b))
    dp(3, int(c))
    dp(4, int(d))

try:
    cnt=10
    while True:
        display(cnt)
        if GPIO.input(sumbtn)==0:
            cnt=cnt+1
            
        if GPIO.input(cdbtn)==0:
            start=time.time()
            while True:
                
                display(cnt)
                if(time.time()-start>0.99):
                    cnt=cnt-1
                    start=time.time()
                if cnt==0:
                    display(0)
                    GPIO.output(led,1)
                    play()
                    flag=1
                    break
        if flag==1:
            break
finally:
    GPIO.cleanup()
    print('by')

        