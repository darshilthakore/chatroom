import os
import json
import requests

from flask import Flask, render_template, request, jsonify, session, url_for, redirect
from flask_session import Session
from flask_socketio import SocketIO, emit, join_room, leave_room, send
from werkzeug.utils import secure_filename
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
app.config["UPLOAD_FOLDER"] = os.getenv("UPLOAD_FOLDER")
socketio = SocketIO(app)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


# users = {'darshil':123}


# channels = {"sports": [["darshil","hey","12:15:30 PM"]], "movies": [["rohan","hola","7:13:12 PM"]] }



#the path which open when user enters the site
@app.route("/")
def index():
	#if a previous user hasn't logged out
	try:
		if session['displayname']:
			print('redirecting to a previous session')
			m = []
			users = db.execute("SELECT username FROM users").fetchall()
			print(f"users from db are {users}")
			for user in users:
				m.append(user)
			print(f"users are {m}")
			return redirect(url_for('mainpage', displayname=session['displayname']))
	# a new user logging in
	except KeyError:
		print("new session")
		return render_template("index.html")


# route to check displayname availability
@app.route("/checkdispname", methods=["POST","GET"])
def checkdispname():
	displayname = request.form.get("displayname")
	if displayname == "":
		return jsonify({"available": False, "msg": "username cannot be empty"})


	users = db.execute("SELECT username FROM users").fetchall()
	print(f"users from db are {users}")
	flag = False
	for user in users:
		print(f'User is {user} - {user[0]}')
		if user[0] == displayname:
			# return jsonify({"available": False, "msg": "this username is not available"})
			flag = False
			break
		else:
			# return jsonify({"available": True, "msg": "username available"}) 
			flag = True
			continue
	if flag == False:
		return jsonify({"available": False, "msg": "this username is not available"})
	else:
		return jsonify({"available": True, "msg": "username available"}) 

	# except KeyError:
	# 	return jsonify({"available": True, "msg": "username available"})

# checking the channel name availability
@app.route("/checkchannelname", methods=["POST","GET"])
def checkchannelname():
	entered_channel = request.form.get("entered_channel")

	channels = db.execute("SELECT name FROM channels").fetchall()
	print(f"channels from db are {channels}")
	flag = False
	for channel in channels:
		print(f'Channel is {channel} - {channel[0]}')

		if channel[0] == entered_channel:
			# return jsonify({"available": False, "msg": "this username is not available"})
			flag = False
			break
		if channel[0] == []:
			flag = False
			break
		else:
			# return jsonify({"available": True, "msg": "username available"}) 
			flag = True
			continue
	if flag == False:
		return jsonify({"available": False, "msg": "channel with same name exists"})
	else:
		return jsonify({"available": True, "msg": "valid channel name"}) 
	# except KeyError:
	# 	return jsonify({"available": True, "msg": "valid channel name"})


#verifiying the user and adding the user to the session
@app.route("/newuser", methods=["POST","GET"])
def newuser():
	displayname = request.form.get("displayname")
	# password = request.form.get("password-login") or " "
	users = db.execute("SELECT username FROM users").fetchall()
	print(f"users from db are {users}")
	# users[displayname] = password
	db.execute("INSERT INTO users (username) VALUES (:username)", {"username": displayname})
	db.commit()
	m = []
	for user in users:
		m.append(user)
	print(f"users are: {m}")
	session['displayname'] = displayname

	return render_template("chat.html",displayname=displayname)

@app.route("/mainpage")
def mainpage():
	return render_template("chat.html", displayname=session['displayname'])

@app.before_request
def make_session_permanent():
	session.permanent = True


#logging out the user
@app.route("/logout")
def logout():
	try:
		users = db.execute("SELECT username FROM users").fetchall()
		print(f"users from db are {users}")
		# users.pop(session['displayname'])
		db.execute("DELETE FROM users WHERE username = :username", {"username": session['displayname']})
		db.commit()
		session.pop('displayname', None)
		return redirect(url_for('index'))
	except KeyError:
		session.pop('displayname', None)
		return redirect(url_for('index'))



#uploading the image to the specified folder
@app.route("/upload", methods=["POST", "GET"])
def upload():
	if request.method == 'POST':
		print("uplaoding file")
		file = request.files['image']
		filename = secure_filename(file.filename)
		print(f"filename is {filename}")
		file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
		return jsonify({"filename": filename})



active_user = {}



#on joining a new channel
@socketio.on('join')
def on_join(data):
    username = session['displayname']
    room = data['room']

    join_room(room)
    print(f"{username} joined {room}")
    #print(f"active user info is : {active_user}")
    m = str(username) + "joined the chat"
    emit('chat join response', m, room=room)


#on leaving a channel
@socketio.on('leave')
def on_leave(data):
    username = session['displayname']
    room = data['room']
    leave_room(room)
    print(f"{username} left {room}")
    m = username + "left the chat"
    emit('chat join response', m, room=room)



#updating the channel list on side bar after adding a new channel
@socketio.on("load channels")
def loadchannels():
	data = []
	channels = db.execute("SELECT name FROM channels").fetchall()
	print(f"channels from db are {channels}")
	for channel in channels:
		data.append(channel[0])

#on connecting to the socket
@socketio.on('connect')
def connect():
	print("socket connected")
	user = session['displayname']
	data = []
	channels = db.execute("SELECT name FROM channels").fetchall()
	print(f"channels from db are {channels}")
	for channel in channels:
		data.append(channel[0])
	print(f"these are the channels {data}")

	emit('response', data, broadcast=False)


#on adding a new channel
@socketio.on('addchannel')
def addchannel(data):
	user = session['displayname']
	print(f"adding a new channel {data}")
	newchannel = data["newchannel"]
	m = []
	db.execute("INSERT INTO channels (name) VALUES (:name)", {"name": newchannel})
	db.commit()
	# channels[newchannel] = []
	channels = db.execute("SELECT name FROM channels").fetchall()
	print(f"channels from db are {channels}")
	for channel in channels:
		m.append(channel[0])
	print(f"updated data structure: {channels}")
	print(f"update list of channels:  {m}")

	emit('response', m, broadcast=True)


#loading messages of the channel which is clicked
@socketio.on('loadmessage')
def loadmessage(data):
	print(f"loading the existing messages of {data}")
	# channel = data["channel"]
	channel = db.execute("SELECT name FROM channels WHERE name = :name", {"name": data["channel"]}).fetchone()
	# print(f"channels from db are {channels}")
	# m = channels[channel]
	print
	m = db.execute("SELECT * FROM messages WHERE channel_name = :channel_name",{"channel_name": channel[0]}).fetchall()
	print(f"messages are {m}")
	if len(m) > 100:
		n = len(m)-100
		del m[0:n]
	print(f"messages are:  {m}")
	m = [dict(row) for row in m]
	print(f"messages are:  {m}")
	emit('message loader', m, broadcast=False, room=channel[0])


#updating the message entered by the user
@socketio.on('updatemessage')
def updatemessage(data):
	print("initialised")
	# channel = data["channel"]
	channel = db.execute("SELECT name FROM channels WHERE name = :name", {"name": data["channel"]}).fetchone()
	print(f"channel to which message is being add to {channel[0]}")
	name = data["name"]
	print(f"name of user: {name} ")

	# channels[channel].append([data["name"], data["msg"], data["time"], data["filename"]])
	db.execute("INSERT INTO messages VALUES (:message, :user, :msg_time, :channel_name, :filename)", {"message": data["msg"], "user": data["name"], "msg_time": data["time"], "channel_name": channel[0], "filename": data["filename"]})
	db.commit()
	# print(f" this is the update channel info : {channels}")
	m = [name, data["msg"], data["time"], data["filename"]]

	print(f"messages of this channel are: {m}")
	emit('new message', m, broadcast=True, room=channel[0])
				



if __name__ == '__main__':
	socketio.run(app)