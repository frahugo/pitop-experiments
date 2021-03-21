import sys
import pathlib
import os
from flask import Flask, redirect
from pitop.pma import Button, LED
from pitop.miniscreen import Miniscreen

button = Button("D0")
led = LED("D1")
miniscreen = Miniscreen()

assets_path = pathlib.Path(__file__).parent.absolute().as_posix()
home_page = open(assets_path + "/home.html").read()

app = Flask(__name__)

# Pi-top interface

def start_blink():
    print("blink")
    led.blink()
    miniscreen.display_multiline_text("Blinking... Press button to stop", font_size=12)
    os.system("aplay " + assets_path + "/bell.wav")


def stop_blink():
    print("stop")
    led.off()
    os.system("espeak \"Excellent. I just turned off the led.\"")
    welcome()

def welcome():
    print("welcome")
    miniscreen.display_image_file(assets_path + "/welcome.gif")

# HTTP endpoints

@app.route('/ping')
def ping():
    return "pong"

@app.route('/')
def home():
    return home_page

@app.route('/blink')
def blink():
    start_blink()
    return redirect("/")

@app.route('/stop')
def stop():
    stop_blink()
    return redirect("/")

button.when_pressed = stop_blink

if __name__ == '__main__':
    welcome()
    app.run(host='0.0.0.0')