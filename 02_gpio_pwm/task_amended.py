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
def dp(digit, number): #자릿수, 숫자를 입력받아 4digits에 띄운다.
    for i in range(4): 
        if i+1==digit :
            GPIO.output(DIGIT_PINS[i], GPIO.LOW)
        else :
            GPIO.output(DIGIT_PINS[i], GPIO.HIGH)
    for i in range(7):
        GPIO.output(SEGMENT_PINS[i], data[number][i])
    time.sleep(0.001)
def play(): #노래 재생
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
    a=x/600 #첫째 자리, 둘째 자리, 셋째 자리, 넷째 자리에 띄울 수를 계산
    dp(1, int(a))
    dp(2, int(b))
    dp(3, int(c))
    dp(4, int(d))

try:
    cnt=0 #설정할 시간을 저장하는 변수
    clkdelay=-1 #꾹 누르면 시간이 너무 빨리 올라가는 것을 막아 주는 변수
    while True:
        
        display(cnt)
        if GPIO.input(sumbtn)==0 and 0.1<time.time()-clkdelay: #sumbtn버튼이 눌리고 전에 버튼을 누른 시간과 현재 시간의 차가 0.1초가 넘으면
            clkdelay=time.time()
            cnt=cnt+1 #시간 추가
            
        if GPIO.input(cdbtn)==0:
            start=time.time() #시간 측정하는 변수
            while True:
                
                display(cnt)
                if(time.time()-start>0.99): #현재 시간과 전 시간의 차가 0.99초가 넘으면(0.01초는 오차 반영)
                    cnt=cnt-1 #1초가 흘렀으므로 1을 빼준다
                    start=time.time()
                if cnt==0:
                    display(0) 
                    GPIO.output(led,1) #LED를 킨다.
                    play() #소리 재생!
                    flag=1 #flag를 1로 만들어 바깥 반복문까지 빠져나갈 수 있게 만들어 준다.
                    break
        if flag==1:
            break
finally:
    GPIO.cleanup()
    print('by')
