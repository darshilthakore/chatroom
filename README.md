# Project 2

Web Programming with Python and JavaScript


This project contains total of '6' files:
1. application.py
2. index.html
3. index.js
4. chat.html
5. chat.js
6. style.css


When the server is started and user opens the website url, then user is redirected to the "index.html" page, where user can enter a unique displayname, which is not used by any other user, i.e. two users cannot have same username. After entering the username, a session for that user is created and then user is redirected to the "chat.html" page.


On the "chat.html" page, user on left side of the page, user can see a navigation panel, where there are options for user to join the existing channels, or create a new unique channel of their own interest, which can be joined by other users as well.

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