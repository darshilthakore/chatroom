import os
import json
import requests

from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
socketio = SocketIO(app)



users = []

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/channels")
def channels():
	return render_template("channels.html")