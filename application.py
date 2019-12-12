import os
import json
import requests

from flask import Flask, render_template, request, jsonify, session, url_for, redirect
from flask_session import Session
from flask_socketio import SocketIO, emit, join_room, leave_room, send

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
socketio = SocketIO(app)



users = {'darshil':123}
# channels = ['#movies', '#sports', '#tvseries', '#hollywood', '#bollywood']
# channel_sports = 
# channel_movies = 
# channels = {"sports": {"darshil": [["hey", "12:15"]]}, "movies": {"rohan": [["hola", "7:13"]]}}

channels = {"sports": [["darshil","hey","12:15"]], "movies": [["rohan","hola","7:13"]] }




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


@app.route("/checkchannelname", methods=["POST","GET"])
def checkchannelname():
	entered_channel = request.form.get("entered_channel")
	try:
		if channels[entered_channel]:
			return jsonify({"available": False, "msg": "channel with same name exists"})
		if channels[entered_channel] == []:
			return jsonify({"available": False, "msg": "channel with same name exists"})

	except KeyError:
		return jsonify({"available": True, "msg": "valid channel name"})


@app.route("/newuser", methods=["POST","GET"])
def newuser():
	displayname = request.form.get("displayname")
	password = request.form.get("password-login")
	users[displayname] = password
	session['displayname'] = displayname

	return render_template("chat.html",displayname=displayname)

@app.before_request
def make_session_permanent():
	session.permanent = True


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

active_user = {}

@socketio.on('join')
def on_join(data):
    username = session['displayname']
    room = data['room']
    # for activechannel in active_user[username]:
    # 	for channel in activechannel:
    # 		if channel ==  room and activechannel[channel] == False:
    # 			activechannel[channel] = True
    # 		else:
    # 			activechannel[channel] = False
    join_room(room)
    print(f"{username} joined {room}")
    #print(f"active user info is : {active_user}")
    m = username + "joined the chat"
    emit('chat join response', m, room=room)

@socketio.on('leave')
def on_leave(data):
    username = session['displayname']
    room = data['room']
    leave_room(room)
    print(f"{username} left {room}")
    m = username + "left the chat"
    emit('chat join response', m, room=room)


@socketio.on("load channels")
def loadchannels():
	data = []
	for channel in channels:
		data.append(channel)

@socketio.on('connect')
def connect():
	print("socket connected")
	user = session['displayname']
	data = []
	for channel in channels:
		data.append(channel)
	print(f"these are the channels {data}")
	# active_user[user] = []
	# for channel in channels:
	# 	active_user[user].append({channel:False})

	# print(f"active user info is : {active_user}")

	emit('response', data, broadcast=False)

@socketio.on('addchannel')
def addchannel(data):
	user = session['displayname']
	print(f"adding a new channel {data}")
	newchannel = data["newchannel"]
	m = []
	channels[newchannel] = []
	for channel in channels:
		m.append(channel)
	print(f"updated data structure: {channels}")
	print(f"update list of channels:  {m}")
	# active_user[user].append({newchannel:False})
	# print(f"active user info is : {active_user}")
	emit('response', m, broadcast=True)


@socketio.on('loadmessage')
def loadmessage(data):
	print(f"loading the existing messages of {data}")
	channel = data["channel"]
	m = channels[channel]
	print(f"messages are:  {m}")
	emit('message loader', m, broadcast=False, room=channel)

@socketio.on('updatemessage')
def updatemessage(data):
	print("initialised")
	channel = data["channel"]
	print(f"channel to which message is being add to {channel}")
	name = data["name"]
	print(f"name of user: {name} ")
	
	# channels[channel][name] = [data["msg"], data["time"]]
	channels[channel].append([data["name"], data["msg"], data["time"]])
	print(f" this is the update channel info : {channels}")
	m = channels[channel]
	# other_users = []
	# for user in active_user:
	# 	if user != name:
	# 		other_users.append(user)
	# for other_user in other_users:
	# 	for channel_name in active_user[other_user]:
	# 		try:
	# 			if channel_name[channel] == False:
	# 				print(f"messages of this channel are :  {m}")
	# 				emit('message loader', m, broadcast=False)
	# 			else:
	# 				print(f"messages of this channel are :  {m} and we are broadcating it to {other_user}")
	# 				emit('message loader', m, broadcast=True)
	# 		except KeyError:
	# 			print("not the channel we're looking for")
	print(f"messages of this channel are: {m}")
	emit('message loader', m, broadcast=True, room=channel)
				



if __name__ == '__main__':
	socketio.run(app)