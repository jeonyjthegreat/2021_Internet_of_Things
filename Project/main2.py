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
led=4
btn=5
led2=17

GPIO.setmode(GPIO.BCM)
GPIO.setup(led, GPIO.OUT)
GPIO.setup(led2, GPIO.OUT)
GPIO.output(led2, GPIO.HIGH)
#GPIO.setup(btn, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(btn, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
#camera=picamera.PiCamera()
cap=cv2.VideoCapture(0)
if not cap.isOpened():
    print('Camera open failed')
    exit()
screen=cv2.imread("cam_white_640_720.png")
path = '/home/pi/src/Project'

def sepia(img):
    img_sepia = np.array(img, dtype=np.float64) # converting to float to prevent loss
    img_sepia = cv2.transform(img_sepia, np.matrix([[0.272, 0.534, 0.131],
                                    [0.349, 0.686, 0.168],
                                    [0.393, 0.769, 0.189]])) # multipying image with special sepia matrix
    img_sepia[np.where(img_sepia > 255)] = 255 # normalizing values greater than 255 to 255
    img_sepia = np.array(img_sepia, dtype=np.uint8)
    return img_sepia
def sharpen(img):
    kernel = np.array([[-1, -1, -1], [-1, 9.5, -1], [-1, -1, -1]])
    img_sharpen = cv2.filter2D(img, -1, kernel)
    return img_sharpen

def HighContrast(img):
    alpha=0.5
    frame_pink = cv2.applyColorMap(frame, cv2.COLORMAP_PINK)
    frame_blur = cv2.GaussianBlur(frame_pink, (0, 0), 2)
    out_frame = cv2.addWeighted(frame_blur, alpha, frame, (1-alpha), 0)
    out_frame = cv2.add(out_frame, 100)
    return out_frame

try:
    while True: 
        reading=analog_read(0)
        ret, frame=cap.read()
        img=frame
        if not ret:
            break
        if reading>=800:
            img=HighContrast(frame)
            #img=pepper(frame)
        elif reading>=600:
            img=sharpen(frame)
        elif reading>=400:
            img=sepia(frame)
        elif reading>=200:
            img=cv2.convertScaleAbs(img, beta=60)
        cv2.imshow('frame', cv2.add(img, screen))
        val=GPIO.input(btn)
        if val==1:
            now_str='photo'+time.strftime("%Y%m%d%H%M%S")+'.jpg'
            cv2.imwrite(now_str, img)
        GPIO.output(led, val)
        if cv2.waitKey(1)==27:
            break
        print(reading)
finally:
    cap.release()
    cv2.destroyAllWindows()
    GPIO.cleanup()