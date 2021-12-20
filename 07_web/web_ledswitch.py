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

@app.route("/<op>")
def led_op(op):
    if op=="on":    
        GPIO.output(LED_PIN2,GPIO.HIGH)
        return render_template("ledon.html")
    if op=="off":
        GPIO.output(LED_PIN2,GPIO.LOW)
        return render_template("ledoff.html")


if __name__=="__main__":
    app.run(host="0.0.0.0")
