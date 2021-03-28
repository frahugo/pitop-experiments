import sys
import os
import pathlib
import multiprocessing
from hud_server import HudServer
from flask import Flask, redirect, request

assets_path = pathlib.Path(__file__).parent.absolute().as_posix()
home_page = open(assets_path + "/home.html").read()

app = Flask(__name__)
queue = multiprocessing.JoinableQueue()
server = HudServer(queue)

server.start()

# Pi-top interface

def welcome():
    print("welcome")
    queue.put("welcome")

def start_blink():
    print("blink")
    queue.put("start_blink")

def stop_blink():
    print("stop")
    queue.put("stop_blink")

def quit():
    print("quit")
    queue.put(None)

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

@app.route('/shutdown')
def shutdown():
    quit()
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError("Not running")
    func()
    return redirect("/")

if __name__ == '__main__':
    welcome()
    app.run(host='0.0.0.0')
