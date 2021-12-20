#모듈 가져오기기
import RPi.GPIO as GPIO
import numpy as np
import spidev
#import picamera
import cv2
import time

spi=spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz=100000
def analog_read(channel):
    ret=spi.xfer2([1,(8+channel)<<4,0])
    adc_out=((ret[1]&3)<<8)+ret[2]
    return adc_out
    #가변저항 값을 가져오는 함수
led=4 #플래시 기능 LED의 핀번호 설정
btn=5 #사진 찍기 기능 스위치의 핀번호 설정
led2=17 # 카메라 전원 여부를 확인하는 기능 LED의 핀번호 설정

GPIO.setmode(GPIO.BCM)
GPIO.setup(led, GPIO.OUT)
GPIO.setup(led2, GPIO.OUT)
GPIO.output(led2, GPIO.HIGH)
#GPIO.setup(btn, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(btn, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
#GPIO 장치들을 사용 가능한 상태로 설정한다.

cap=cv2.VideoCapture(0)

if not cap.isOpened():
    print('Camera open failed')
    exit() #카메라 장착 여부 확인

screen=cv2.imread("cam_white_640_720.png")
#디지털 카메라 디자인 가져오기

path = '/home/pi/src/Project'

def sepia(img):
    img_sepia = np.array(img, dtype=np.float64) # converting to float to prevent loss
    img_sepia = cv2.transform(img_sepia, np.matrix([[0.272, 0.534, 0.131],
                                    [0.349, 0.686, 0.168],
                                    [0.393, 0.769, 0.189]])) # multipying image with special sepia matrix
    img_sepia[np.where(img_sepia > 255)] = 255 # normalizing values greater than 255 to 255
    img_sepia = np.array(img_sepia, dtype=np.uint8)
    return img_sepia
    #Sepia 필터를 사용하기 위한 함수

def sharpen(img):
    kernel = np.array([[-1, -1, -1], [-1, 9.5, -1], [-1, -1, -1]])
    img_sharpen = cv2.filter2D(img, -1, kernel)
    return img_sharpen
    #Sharpen 필터를 사용하기 위한 함수

def pink(img):
    alpha=0.5
    frame_pink = cv2.applyColorMap(frame, cv2.COLORMAP_PINK)
    frame_blur = cv2.GaussianBlur(frame_pink, (0, 0), 2)
    out_frame = cv2.addWeighted(frame_blur, alpha, frame, (1-alpha), 0)
    out_frame = cv2.add(out_frame, 100)
    return out_frame
    #핑크핑크한 필터를 사용하기 위한 함수

try:
    while True: #ESC키나 Ctrl+C가 입력될 때까지 무한 반복
        reading=analog_read(0) #가변저항 값을 가져온다.
        ret, frame=cap.read() #카메라에서 입력을 받는다. frame은 원본본
        img=frame #img 변수는 필터를 적용한 사진으로, 화면에 띄워지고 실제로 사진으로 저장되는 이미지를 받는 함수이다. 

        if not ret:
            break

        if reading>=800:
            img=pink(frame)
            #가변저항 값이 800 이상이면, 핑크핑크한 필터를 씌운다.

        elif reading>=600:
            img=sharpen(frame)
            #가변저항 값이 800 미만 600 이상이면, sharpen 필터를 씌운다.

        elif reading>=400:
            img=sepia(frame)
            #가변저항 값이 600 미만 400 이상이면, sepia 필터를 씌운다.

        elif reading>=200:
            img=cv2.convertScaleAbs(img, beta=60)
            #가변저항 값이 400 미만 200 이상이면, 이미지 밝기를 올린다.

        #가변저항 값이 200 미만이면, 필터를 씌우지 않은, 원본 이미지를 출력과 저장에 사용한다.

        cv2.imshow('frame', cv2.add(img, screen)) 
        #이미지와 디지털 카메라 디자인을 합친 이미지를 디지털 카메라 화면에 띄운다.

        val=GPIO.input(btn)
        #스위치의 값을 val이라는 변수로 받는다.
        if val==1:
            now_str='photo'+time.strftime("%Y%m%d%H%M%S")+'.jpg'
            cv2.imwrite(now_str, img)
            #스위치를 누르면 img 변수의 사진을 저장한다.
        GPIO.output(led, val) #스위치를 누르면 사진을 찍는다는 것을 알려주는 플래시를 터뜨린다.
        if cv2.waitKey(1)==27:
            break
            #ESC키를 누르면 이 반복문을 빠져나온다.
        #print(reading) 가변저항 테스트를 위한 출력이지만, 필요 없으므로 주석 처리.
finally:
    cap.release()
    cv2.destroyAllWindows()
    GPIO.cleanup()