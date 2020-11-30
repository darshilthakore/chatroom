    	document.addEventListener('DOMContentLoaded', () => {
	   		var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);


	   		//check if the tab was closed without logging out, and retrieve the channel and its messages
	   		if (localStorage.getItem('retrieve_channel')) {
	   			console.log(localStorage.getItem('retrieve_channel'));
	   			const load_closed_channel = localStorage.getItem('retrieve_channel');
	   			socket.emit('join', {'room': load_closed_channel});
	   			socket.emit('loadmessage', {'channel': load_closed_channel});
	   			document.querySelector('.heading').innerHTML = load_closed_channel;
				document.querySelector('[name="message"]').value = "";
				document.querySelector('#sendmessage').disabled = false;
				document.querySelector('[name="message"]').disabled = false;
				console.log('retrieving the channel info');
			

	   		}


	   		socket.on('connect', () => {
	   	
	   			if (!sessionStorage.getItem('channel')){
	   				document.querySelector('#sendmessage').disabled = true;
	   				document.querySelector('[name="message"]').disabled = true;
	   			}
	   			
	   			document.querySelector('#channel-btn').disabled = true;

	   			// entering the channel name and checking availability with AJAX
	   			document.querySelector('[name="newchannel"]').onkeyup = () => {
	   				const newchannel = document.querySelector('[name="newchannel"]').value;
	   				if (newchannel.length > 0) {
	   					document.querySelector('#channel-btn').disabled = false;
	   				} else {
	   					document.querySelector('#channel-btn').disabled = true;
	   				}
	   				const request = new XMLHttpRequest();
					request.open('POST', '/checkchannelname');
					request.onload = () => {
						const response = JSON.parse(request.responseText);
						const msg = `${response.msg}`
						if (response.available) {
							document.querySelector('.validation').innerHTML = msg;
						} else {
							document.querySelector('.validation').innerHTML = msg;
							document.querySelector('#channel-btn').disabled = true;
						}



					};

					//send the displayname  along with the request
					const data = new FormData();
					data.append('entered_channel', newchannel);
					//send request

					request.send(data);



	   			};
	   			//create channel
	   			document.querySelector('#channel-btn').onclick = () => {
	   				const newchannel = document.querySelector('[name="newchannel"]').value;
		   			if (newchannel.length > 0) {
		   				socket.emit('addchannel', {'newchannel': newchannel});
		   			}
		   			document.querySelector('[name="newchannel"]').value = "";
	   			}



	   		});	
	   		//on sending a message
   			document.querySelector('#userinput').onsubmit = () => {
				if (document.querySelector('#attachment').value == '') {
					const channel = sessionStorage.getItem('channel');
		    		const name = document.querySelector('#displayname').getAttribute('data-displayname');
		    		const msg = document.querySelector('[name="message"]').value;
		    		const filename = '';
		    		const time = timeStamp();
		    		console.log("sending a solo text");
		    		socket.emit('updatemessage', {'channel':channel, 'name':name, 'msg':msg, 'time':time, 'filename':filename});
		    		return false;
				} else {
					const request = new XMLHttpRequest();
		    		const image = document.querySelector('#attachment').files[0];
		    		request.open('POST', '/upload');

		    		request.onload = () => {
		    			const data = JSON.parse(request.responseText);
		    			const filename = `${data.filename}`
		    			const channel = sessionStorage.getItem('channel');
			    		const name = document.querySelector('#displayname').getAttribute('data-displayname');
			    		const msg = document.querySelector('[name="message"]').value;
		    			const time = timeStamp();
		    			console.log("on load request");
		    			console.log(filename);
			    		//message(n,d,t);
			    		document.querySelector('[name="message"]').value = "";
			    		socket.emit('updatemessage', {'channel':channel, 'name':name, 'msg':msg, 'time':time, 'filename':filename});
		    		}
		    		//console.log(window.filename);
		    		//return false;
		    		const data = new FormData();
		    		data.append('image', image);
		    		request.send(data);
		    		document.querySelector('#attachment').value = '';
		    		return false;

				}
	    		

	    		
	    	}

	    	//on clicking an existing channel
   			document.addEventListener('click', event => {
   				const element = event.target;
   				if (element.className === 'list'){
   					if (sessionStorage.getItem('channel')) {
   						const channel = sessionStorage.getItem('channel');
   						socket.emit('leave', {'room': channel});
   						sessionStorage.clear();

   					}

   					
   					new_channel = element.getAttribute('data-channel');
   					//socket.emit('leave', {'room':channel});
   					sessionStorage.setItem('channel', new_channel);
   					localStorage.setItem('retrieve_channel', new_channel);
   					//const name = document.querySelector('#displayname').getAttribute('data-displayname');
   					socket.emit('join', {'room': new_channel});
   					//document.querySelector('#chatarea').innerHTML = "";
   					socket.emit('loadmessage', {'channel': new_channel});
   					document.querySelector('.heading').innerHTML = new_channel;
   					document.querySelector('[name="message"]').value = "";
   					document.querySelector('#sendmessage').disabled = false;
	   				document.querySelector('[name="message"]').disabled = false;
   				}
   			});


	   		
   			//updates the existing channel lists
	   		socket.on('response', data => {
	   			document.querySelector('.channel-list').innerHTML = "";
	   			for(i = 0; i < data.length; i++) {
	   				channel(data[i]);
	   			}
	   		});

	   		//loads the messages in chat area
	   		socket.on('message loader', data => {
	   			document.querySelector('#chatarea').innerHTML = "";
	   			for (i = 0; i < data.length; i++) {
	   				msg_details = data[i];
	   				const user = msg_details['user'];
	   				const msg = msg_details['message'];
	   				const time = msg_details['msg_time'];
	   				const filename = msg_details['filename'];
	   				message(user,msg,time,filename);
	   				window.scrollBy(0, document.body.offsetHeight);
	   			}

	   		});


	   		socket.on('new message', data => {
	   			new_msg_details = data;
	   			const user = new_msg_details[0];
	   			const msg = new_msg_details[1];
	   			const time = new_msg_details[2];
	   			const filename = new_msg_details[3];
	   			entered_message(user,msg,time,filename);
	   			window.scrollBy(0, document.body.offsetHeight);
	   		});

	   		socket.on('chat response', data => {
	   			const msg = data;
	   			document.querySelector('#chatarea').innerHTML += msg;
	   		});


	   		//template for channels
	    	const channel_template = Handlebars.compile(document.querySelector('#channel-list').innerHTML);
	    	function channel(channel) {
	    		const ch = channel_template({'channel': channel});
	    		document.querySelector('.channel-list').innerHTML += ch;
	    	}


	    	//function to get current timestamp
	    	function timeStamp() {
	    		var d = new Date();
	    		var n = d.toLocaleTimeString();
	    		return n;
			}


			//template for messages
			const msg_template = Handlebars.compile(document.querySelector('#message').innerHTML);
	    	function message(displayname,message,time,filename) {
	    		const msg = msg_template({'displayname': displayname, 'message': message, 'time': time, 'filename': filename});
	    		document.querySelector('#chatarea').innerHTML += msg;
	    	}


	    	//template for entered messages
			const entered_msg_template = Handlebars.compile(document.querySelector('#entered_message').innerHTML);
	    	function entered_message(displayname,message,time,filename) {
	    		const msg = entered_msg_template({'displayname': displayname, 'message': message, 'time': time, 'filename': filename});
	    		document.querySelector('#chatarea').innerHTML += msg;
	    	}

	    	document.querySelector('.heading').onclick = () => {
	    		window.scrollBy(0,0);

	    	}

	    	

	    	document.querySelector('#logout').onclick = () => {
	    		localStorage.clear();
	    		sessionStorage.clear();
	    	}

    	});