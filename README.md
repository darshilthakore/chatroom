# Project 2

Web Programming with Python and JavaScript


This project contains total of '6' files:
1. application.py
2. index.html
3. index.js
4. chat.html
5. chat.js
6. style.css


When the server is started and user opens the website url, then user is redirected to the `"index.html"` page, where user can enter a unique displayname, which is not used by any other user, i.e. two users cannot have same username. This functionality is implemented in the `"index.js"` file, where an AJAX request is made to the server by sending the name enetered by the user to the path `"/checkdispname"` in `"application.py"`. In the `"application.py"` at the `"/checkdispname"` route, the name entered by the user is checked with the global dictionary declared in server `"users"`. If same user is there, then response is sent that username is unavailable, else it is available. This is an example of the user dictionary with some users who have logged in --- ` users are: ['darshil', 'brian', 'alice'] `


After entering the username and clicking enter, the username which is entered is sent to the route `'/newuser'` on the server, where a `newuser` function store this username in the dictionary "users" and creates a session for that user using the username like this way `session['displayname'] = displayname`, then user is redirected to the `"chat.html"` page.

In the chat.html page, we have defined three handlebar templates:
1. Channel Buttons `id="channel-list"`
2. Messages which will be loaded when channel is clicked. `id="message"`
3. Message which will be added by user. `id="entered_message"`

The channel template will update the channel list with new channel button in the `channel-list`. The `message` template will generate the messages from the information passed to it and will display the messages in `chatarea`. The `entered_message` works in the same way as that for `message`, which will add the message entered by the user from the form area, which includes and option to input text, image and a send button.


In the "chat.html" page, user can see a navigation panel on the left, where there is `<div>` of class `"channel-list"`, where all the existing channels and channels that are to be added will be displayed. There is an input box and a button, where user can enter channel of there own. And lastly, there is a logout button, which when clicked will redirect the user to the route `"/logout"` in `application.py`, which will destroy the session for the user by popping out -- `session.pop('displayname', None)`.

`"chat.js"` file includes the javascript code.
Whenever the `chat.html` is loaded, a new `socket` is created and the document waits for the socket to get connected.
When the socket gets connected, it loads the list of channels that are already present through the event `on(connect)` in server and then emits the data to the event `response` in `chat.js` which will use handlebar `channel-list` to load the channels. 



The div with `id="chatarea"` is the section, where the messages are gonna get displayed.



Now when user types a new channel, which he wants to add, an ajax request is send to the server at the path `/checkchannelname`, to check the channel availability just like in case for username. The `/checkchannelname` will check with the existing channels whether the new channel is conflicting with any existing channels. If channel is not available, then the button to submit channel name is disabled, else user is allowed to add.



On clicking the create channel button, the name of the channel is emitted to the event `add channel` in `application.py`, which will update the channel list in the server with the new channel and then emit the updated channel list to the `response` event in `chat.js` with parameter for `broadcast=True`, which will update the channel-list of the page with the newly added channel and it will be updated for all the users, which are connected because of the parameter `broadcast=True`.



Now on clicking any existing channel button will result on sending the channel information to the event `join` and `loadmessage` in the server, which will make the user in session to join the room(i.e the channel) by a function inbuilt in flask-socketio called `join_room()` , which user selected, on the other hand `loadmessage` will load the messages of the selected channel and emit this data to the event `message loader` in the chat.js. Note that here `broadcast=False` as this will load message only for the user, who clicked the channel and argument `room=channel` denotes the room which the user currently is in. Whenever a channel is selected, the channel name is stored in the `localStorage` for the browser `localStorage.setItem('retrieve_channel', new_channel);`. In case we close the browser tab/window without logging out, then localStorage is called to check if the channel is stored in key `retrieve_channel`, if it is, then that channel is loaded alongwith the messages, now when user logs out, all the localStorage and sessionStorage is cleared.

If user switches to other channel by clicking the other channel, then a condition will be checked whether localStorage has any saved channel, which eventually would be there, as we already had one channel selected before. Now this channel information from localStorage is used to leave that previous channel through the event `leave` on the server, which has function `leave_room()`, for removing the user from the room. Next the join event will be performed for this newly selected channel and `join_room()` for this channel will be performed to make the user join this channel, and then `loadmessage` will load messages just the way described above section. Also now the `localStorage` information for this new channel will be updated with the new channel.


`message loader` in `chat.js` will use the data fetched from the server, and will pass it to function `message`, which will generate the message and append it to the `chatarea`, here the `msg_template` is the handle bar template for the message, which is defined in the `chat.html`, which includes information like username, message, image(if any) and timestamp of the message.

Now when a user has selected a channel, he can send his own message in this channel. On clicking the send button, it is checked whether an image is uploaded or not, if yes, then an AJAX request is made to the server at path `'/upload'`, where the image is uploaded in the `"static"` folder of the project directory, and `filename` is returned as the AJAX response. This response alongwith other data like the message entered by user, timestamp, channel is sent to the event `updatemessage` in the server `application.py`.

`updatemessage` event will update the messages stored in the dictionary `channels` (example for message in a channel --- `[['brian', '', '2:12:03 PM', 'azpi.png'], ['alice', 'hi', '2:15:46 PM', ''], ['brian', 'hey alice', '2:15:57 PM', ''], ['alice', 'hi njfnlkdnlk', '2:16:06 PM', ''], ['alice', 'hi njfnlkdnlk', '2:16:14 PM', 'alonso.png']]`) for the channel on which message was sent, and will send the latest message of this channel(i.e the one that user entered) to the event `new message` in chat.js. `new message` will fetch the data and pass it to the function `entered_message` which works similarly as the function `message` described above, and will generate a message template and append it to the list of messages in the chatarea. Note here `broadcast=True`, which means that when two or more users are in same room(checked by the condition `room=room`, while performing emit from server), changes in the chat area or any new messages which are added will reflect for all the users giving a real time chat vibes.




Here is a short summary for `application.py` fuctions and events and their return and emit response:

#the path which open when user enters the site
@app.route("/")
def index():
#returns the index page, or the chat page if a session exists


# route to check displayname availability
@app.route("/checkdispname", methods=["POST","GET"])
def checkdispname():
#returns availability response

# checking the channel name availability
@app.route("/checkchannelname", methods=["POST","GET"])
def checkchannelname():
#returns availability response



#verifiying the user and adding the user to the session
@app.route("/newuser", methods=["POST","GET"])
def newuser():



#logging out the user
@app.route("/logout")
def logout():


#uploading the image to the specified folder
@app.route("/upload", methods=["POST", "GET"])
def upload():
#return filename as AJAX response


#on joining a new channel
@socketio.on('join')
def on_join(data):
#performs join_room() for a session

#on leaving a channel
@socketio.on('leave')
def on_leave(data)
#performs leave_room() for a session


#on connecting to the socket
@socketio.on('connect')
def connect():
#sends the current channels to the event `response` in chat.js


#on adding a new channel
@socketio.on('addchannel')
def addchannel(data):
#updates current channel list and sends the new channels to event `response` in chat.js


#loading messages of the channel which is clicked
@socketio.on('loadmessage')
def loadmessage(data):
#fetches the messages of the channel which is clicked and sends it to the event `message loader` in chat.js


#updating the message entered by the user
@socketio.on('updatemessage')
def updatemessage(data):
#adds the entered message and updates it on the server,then fetches the latest message of the channel which is clicked and sends it to the event `new message` in chat.js




Here is a short summary for `chat.js` functions and events and their emit response:



#check if the tab was closed without logging out, and retrieve the channel and its messages
if (localStorage.getItem('retrieve_channel'))
socket.emit('join', {'room': load_closed_channel});
socket.emit('loadmessage', {'channel': load_closed_channel});


socket.on('connect', ()
# entering the channel name and checking availability with AJAX


#on creating a channel
socket.emit('addchannel', {'newchannel': newchannel});


#on sending a message
socket.emit('updatemessage', {'channel':channel, 'name':name, 'msg':msg, 'time':time, 'filename':filename});



#on clicking an existing channel
socket.emit('leave', {'room': channel});
sessionStorage.setItem('channel', new_channel);
localStorage.setItem('retrieve_channel', new_channel);
socket.emit('join', {'room': new_channel});
socket.emit('loadmessage', {'channel': new_channel});


#updates the existing channel lists
socket.on('response'

#loads the messages in chat area
socket.on('message loader'
message(user,msg,time,filename);

socket.on('new message', data
entered_message(user,msg,time,filename);

#template for channels
function channel(channel)


#function to get current timestamp
function timeStamp() 


#template for messages
function message(displayname,message,time,filename)

#template for entered messages
function entered_message(displayname,message,time,fi
lename)

#logging out
document.querySelector('#logout').onclick = () => {
	    		localStorage.clear();
	    		sessionStorage.clear();
	    	}




How to run:

1. Open the terminal in change to project path.
2. You'll need a secret key for running, generate that in python interpreter as follows:

import os
os.urandom(24)

which will give you a random key say : '\x1aS:\x15\xf1\xbdYZz\xb2W\xab|\x88e\xc1\xe4\x1a\x13\r\xffz\xd5E'

3. export it

export SECRET_KEY='\x1aS:\x15\xf1\xbdYZz\xb2W\xab|\x88e\xc1\xe4\x1a\x13\r\xffz\xd5E'

4. set application.py 

export FLASK_APP=application.py

5. set an upload path(to store the images uploaded by users as message on the server)

export UPLOAD_FOLDER=static

6. run the project

python3 application.py


7. type the url in browser

http://127.0.0.1:5000/


The "style.css" contains the styling part for page, while "index.js" and "chat.js" deal with the javascript and "application.py" is the server side code.