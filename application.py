import os
import json
import requests

from flask import Flask, render_template, request, jsonify, session, url_for, redirect
from flask_session import Session
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
socketio = SocketIO(app)



users = {'darshil':123}
# channels = ['#movies', '#sports', '#tvseries', '#hollywood', '#bollywood']
# channel_sports = 
# channel_movies = 
channels = {"sports": {"darshil": "hey"}, "movies": {"rohan": "hola"} }




@app.route("/")
def index():
    return render_template("index.html")


# route to check displayname availability
@app.route("/checkdispname", methods=["POST","GET"])
def checkdispname():
	displayname = request.form.get("displayname")
	if displayname == "":
		return jsonify({"available": False, "msg": "username cannot be empty"})
	# getting the displayname from the form
	# if displayname in users:
	# 	prompt = "displayname not available"
	# 	return jsonify(prompt)
	# prompt = "username available"
	# return jsonify(prompt)
	try:
		if users[displayname]:
			return jsonify({"available": False, "msg": "this username is not available"})

	except KeyError:
		return jsonify({"available": True, "msg": "username available"})


@app.route("/newuser", methods=["POST","GET"])
def newuser():
	displayname = request.form.get("displayname")
	password = request.form.get("password-login")
	users[displayname] = password
	session['displayname'] = displayname

	return render_template("chat.html",displayname=displayname)

# @app.route("/channels")
# def channels():
# 	return render_template("channels.html")


# @app.route("/channellists", methods=["POST","GET"])
# def channellists():

# 	return jsonify(channels)

# @app.route("/newchannel", methods=["POST","GET"])
# def newchannel():
# 	channel = request.form.get("channel")
# 	channel = '#' + str(channel)
# 	channels.append(channel)
# 	return channels[-1]

# @app.route("/updatechannel", methods=["POST","GET"])
# def updatechannel():
# 	m = channels[-1]
# 	return jsonify(m)


@socketio.on("load channels")
def loadchannels():
	data = []
	for channel in channels:
		data.append(channel)

@socketio.on('connect')
def connect():
	print("socket connected")
	data = []
	for channel in channels:
		data.append(channel)
	print(data)
	emit('response', data, broadcast=False)

@socketio.on('addchannel')
def addchannel(data):
	print(f"adding a new channel {data}")
	newchannel = data["newchannel"]
	m = []
	m.append(newchannel)
	channels[newchannel] = {}
	print(channels)
	print(m)
	emit('response', m, broadcast=True)


if __name__ == '__main__':
	socketio.run(app)