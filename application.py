import os
import json
import requests

from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
socketio = SocketIO(app)



users = ["darshil"]


@app.route("/")
def index():
    return render_template("index.html")


# route to check displayname availability
@app.route("/checkdispname", methods=["POST"])
def checkdispname():

	# getting the displayname from the form
	displayname = request.form.get("displayname")
	if displayname in users:
		prompt = "displayname not available"
		return jsonify(prompt)
	prompt = "username available"
	return jsonify(prompt)


@app.route("/channels")
def channels():
	return render_template("channels.html")