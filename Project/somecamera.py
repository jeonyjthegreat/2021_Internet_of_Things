import RPi.GPIO as GPIO
import spidev
import numpy as np
import cv2
from datetime import time
import random


#핀 선언 및 핀모드 설정
LED_PIN = 16
BUTTON_PIN= 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

#카메라 작동
cam=cv2.VideoCapture(0)

#얼굴 검출 코드 불러오기
face_cascade = cv2.CascadeClassifier(
    './xml/face.xml'
)

#캠 틀 가져오기
"""cam_img = cv2.imread("cam_640_720.png")
cam_white = cv2.imread("cam_white_640_720.png")
cam_black = cv2.imread("cam_white_640_720.png")"""

#가변저항 읽기 위한 채널 설정
spi= spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz=10000

def analog_read(channel):
  ret = spi.xfer2([1, (channel+8)<<4, 0])
  adc_out = ((ret[1]&3)<<8)+ret[2]
  return adc_out

#만약 카메라 작동이 되지 않으면 종료
if not cam.isOpened():
    print('Camera open failed')
    exit()

#노이즈&촬영필터
def add_noise(img):
 
    # Getting the dimensions of the image
    row , col, channel = img.shape
    # Randomly pick some pixels in the
    # image for coloring them white
    # Pick a random number between 300 and 10000
    number_of_pixels = random.randint(300, 10000)
    for i in range(number_of_pixels):
       
        # Pick a random y coordinate
        y_coord=random.randint(0, row - 1)
         
        # Pick a random x coordinate
        x_coord=random.randint(0, col - 1)
         
        # Color that pixel to white
        img[y_coord][x_coord] = 255
         
    # Randomly pick some pixels in
    # the image for coloring them black
    # Pick a random number between 300 and 10000
    number_of_pixels = random.randint(300 , 10000)
    for i in range(number_of_pixels):
       
        # Pick a random y coordinate
        y_coord=random.randint(0, row - 1)
         
        # Pick a random x coordinate
        x_coord=random.randint(0, col - 1)
         
        # Color that pixel to black
        img[y_coord][x_coord] = 0
         
    return img

#가변저항 값에 따른 필터 함수
def filter(reading, frame):
    frame_copy=frame
    #원본 이미지
    if reading < 256:
        out_frame=frame
            
    #언샤크 필터
    elif reading < 512:
        """frame_ycrcb = cv2.cvtColor(frame, cv2.COLOR_BGR2YCrCb)
        frame_f = frame_ycrcb[:, :, 0].astype(np.float32)
        blr = cv2.GaussianBlur(frame_f, (0, 0), 2.0)
        frame_ycrcb[:, :, 0] = np.clip(2. * frame_f - blr, 0, 255).astype(np.uint8)

        out_frame = cv2.cvtColor(frame_ycrcb, cv2.COLOR_YCrCb2BGR)"""

        kernel = np.array([[-1, -1, -1], [-1, 9.5, -1], [-1, -1, -1]])
        out_frame = cv2.filter2D(frame, -1, kernel)

                
    #뽀샤시 필터
    elif reading < 768:
        alpha=0.8
        frame_pink = cv2.applyColorMap(frame, cv2.COLORMAP_PINK)
        frame_blur = cv2.GaussianBlur(frame_pink, (0, 0), 2)
        out_frame = cv2.addWeighted(frame_blur, alpha, frame, (1-alpha), 0)
        out_frame = cv2.add(out_frame, 50)
    
    #소금&후추 필터를 이용한 사진기 필터
    else:
        noise_frame=add_noise(frame)
        add_frame = cv2.addWeighted(frame, 0.5, noise_frame, 0.5, 0)

        cam_img = cv2.imread('cam_640_720.png', 1)
        roi = add_frame[0, 0]#배경이미지의 변경할(다음 로고 넣을) 영역
        mask = cv2.cvtColor(cam_img, cv2.COLOR_BGR2GRAY)#로고를 흑백처리
        #이미지 이진화 => 배경은 검정. 글자는 흰색
        mask[mask[:]==255]=0
        mask[mask[:]>0]=255
        mask_inv = cv2.bitwise_not(mask) #mask반전.  => 배경은 흰색. 글자는 검정
        daum = cv2.bitwise_and(cam_img, cam_img, mask=mask)#마스크와 로고 칼라이미지 and하면 글자만 추출됨
        back = cv2.bitwise_and(roi, roi, mask=mask_inv)#roi와 mask_inv와 and하면 roi에 글자모양만 검정색으로 됨
        dst = cv2.add(daum, back)#로고 글자와 글자모양이 뚤린 배경을 합침
        add_frame[0, 0] = dst  #roi를 제자리에 넣음
        out_frame = add_frame

    return out_frame

try:
    while True:
        #가변저항값 읽기
        reading = analog_read(0)

        #프레임에변수 카메라 출력 대입
        ret, frame = cam.read()

        #원본이미지에서 얼굴 검출 후  
        frame_filter = filter(reading, frame)

        """#원본이미지에서 얼굴 검출 후, 미리보기 이미지에 얼굴 인식 범위 그리기
        face = face_cascade.detectMultiScale(frame, 1.3, 5)
        for(x, y, w, h) in face:
        
            cv2.rectangle(
                frame_preview, ((x+w/2)-50, (y+h/2)-50),
                ((x+w/2)+50, (y+h/2)+50), (255, 255, 0), 2
            )"""
        
        #preview 출력
        cv2.imshow('preview', frame_filter)
        
        #사진 촬영
        if GPIO.input(BUTTON_PIN)==1:
            #파일명 설정을 위해 날짜 불러오기
            now_str='photo'+time.strftime("%Y%m%d%H%M%S")
            cv2.imwrite(now_str, frame_filter)


        #만약 esc를 누르면 종료
        if cv2.waitKey(10)==13:
            break

        

finally:
    cv2.destroyAllWindows()