from flask import Flask
from flask.templating import render_template
import RPi.GPIO as GPIO
LED_PIN=4
LED_PIN2=5
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)
GPIO.setup(LED_PIN2, GPIO.OUT)

app=Flask(__name__)

@app.route("/")
def hello_world():
    return render_template("led.html")
@app.route("/led/<op>")
def led_op(op):
    if op=="on":
        GPIO.output(LED_PIN,GPIO.HIGH)
        return "REDON"
    if op=="off":
        GPIO.output(LED_PIN,GPIO.LOW)
        return "REDOFF"

if __name__=="__main__":
    app.run(host="0.0.0.0")
