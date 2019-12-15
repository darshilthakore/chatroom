# Project 2

Web Programming with Python and JavaScript


This project contains total of '6' files:
1. application.py
2. index.html
3. index.js
4. chat.html
5. chat.js
6. style.css


When the server is started and user opens the website url, then user is redirected to the "index.html" page, where user can enter a unique displayname, which is not used by any other user, i.e. two users cannot have same username. This functionality is implemented in the "index.js" file, where an AJAX request is made to the server by sending the name enetered by the user to the path "/checkdispname" in "application.py". In the "application.py" at the "/checkdispname" route, the name entered by the user is checked with the global dictionary declared in server "users". If same user is there, then response is sent that username is unavailable, else it is available.


After entering the username and clicking enter, the username which is entered is sent to the route '/newuser' on the server, where a function store this username in the dictionary "users" and creates a session for that user using the username, then user is redirected to the "chat.html" page.

In the "chat.html" page, user can see a navigation panel on the left, where there is <div> of class "channel-list", where all the existing channels and channels that are to be added will be displayed. There is an input box and a button, where user can enter channel of there own. And lastly, there is a logout button, which when clicked will direct the user to the route "/logout" is application.py, which will destroy the session for the user.

"chat.js" file includes the javascript code.
Whenever the chat.html is loaded, a new `socket` is created and the document waits for the socket to get connected.
When the socket gets connected, it loads the list of channels that are already present through the event `connect` in server by emiting the data to the event `response` in chat.js which loads the channel list. 



The div with id="chatarea" is the section, where the messages are gonna get displayed.



Now when user types a new channel, which he wants to add, an ajax request is send to the server, to check the channel availability just like in case for username. If channel is not available, then the button to submit channel name is disabled, else user is allowed to add.



In clicking the create channel button, the name of the channel is emitted to the even `add channel` in application.py, which will update the channel list in the server with the new channel and then emit the updated channel list to the `response` event in chat.js with parameter for `broadcast=True`, which will update the channel-list of the page with the new added channel and it will be updated for all the users, which are connected because of the parameter `broadcast=True`.



Now on clicking any existing channel button will result on sending the channel information to the event `join` and `loadmessage` in the server, which will make the user in session to join the room(i.e the channel) by a function inbuilt in flask-socket called `join_room()` , which he selected, on the other hand `loadmessage` will load the messages of the selected channel and emit this data to the event `message loader` in the chat.js. Note that here `broadcast=False` as this will load message only for the user, who clicked the channel and argument `room=channel` denotes the room which is operated. Whenever a channel is selected, the channel name is stored in the `localStorage` for the browser `localStorage.setItem('retrieve_channel', new_channel);`. In case we close the browser tab/window without logging out, then localStorage is called to check if the channel is stored, if it is, then that channel is loaded alongwith the messages, now when user logs out, all the localStorage and sessionStorage is cleared.

If user switches to other channel by clicking the other channel, then a condition will be checked whether localStorage has any saved channel, which eventually would be there, as we already had one channel selected before. Now this channel information from localStorage is used to leave that previous channel through the even `leave` on the server, which has function leave_room(), for removing the user from the room. Next the join event will be performed for this newly selected channel and it's messages will be loaded just the way described above. Also now the localStorage information for this new channel will be updated with the new channel.


`message loader` will use the data fetched from the server, and will pass it to function `message`, which will generate the message and append it to the chatarea, here the `msg_template` is the handle bar template for the message, which is defined in the chat.html, which includes information like username, message, image(if any) and timestamp of the message.

Now when a user has selected a channel, he can send his own message in this channel. On clicking the send button, it is checked whether an image is uploaded or not, if yes, then an AJAX request is made to the server at path '/upload', where the image is uploaded in the "static" folder of the project directory, and filename is returned as the AJAX response. This response alongwith other data like the message entered by user, timestamp, channel is sent to the event `updatemessage` in the server.

`updatemessage` event will update the messages stored in the dictionary `channels` for the channel on which message was sent, and will send the latest message of this channel(i.e the one that user entered) to the event `new message` in chat.js. `new message` will fetch the data and pass it to the function `entered_message` which works similarly as the function `message` described above, and will generate a message template and append it to the list of messages in the chatarea. Note here `broadcast=True`, which means that when two or more users are in same room(checked by the condition `room=room`, while performing emit from server), changes in the chat area or any new messages which are added will reflect for all the users giving a real time chat vibes.

On clicking the channel, the user now can see the existing messages of that channel, alongwith an option to send the message of their own in that channel, which is displayed to other users connected to the same channel as well in real time, when the user sends the message.


Also an option for sending an image as a message is also provided to the user, so that they can share an image over a channel to other users, who have joined.


All the messages which are sent through the channels are broadcasted to the users connected to the same channel, and the messages are also stored over the server, so that when a new user joins a channel on which he/she was not during the time when messages were sent, then they could load and see them.


A logout option is also provided, which destroys the session of that user. In case user closes the window without logging out, and tries to open the window again with the url, then the page will redirect him/her to the last channel he/she was on and there'll be no need to login again as session is not yet destroyed. This is implemented with the concepts of sessionStorage and localStorage.




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