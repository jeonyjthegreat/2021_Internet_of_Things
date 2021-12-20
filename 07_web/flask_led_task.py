from flask import Flask, render_template
import RPi.GPIO as GPIO
LED_PIN=4
LED_PIN2=5
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)
GPIO.setup(LED_PIN2, GPIO.OUT)

app=Flask(__name__)

@app.route("/")
def hello_world():
    return render_template("led2.html")

@app.route("/led/<col>/<op>")
def led_op(col, op):
    if col=="red" and op=="on":
        GPIO.output(LED_PIN,GPIO.HIGH)
        return "RED LED ON"
    if col=="red" and op=="off":
        GPIO.output(LED_PIN,GPIO.LOW)
        return "RED LED OFF"
    if col=="blue" and op=="on":
        GPIO.output(LED_PIN2,GPIO.HIGH)
        return "BLUE LED ON"
    if col=="blue" and op=="off":
        GPIO.output(LED_PIN2,GPIO.LOW)
        return "BLUE LED OFF"


if __name__=="__main__":
    app.run(host="0.0.0.0")
