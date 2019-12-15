document.addEventListener('DOMContentLoaded', () => {

	//checking the displayname availability
	document.querySelector('#newbtn').disabled = true;
	document.querySelector('[name="displayname"]').onkeyup = () => {


		
		const displayname = document.querySelector('[name="displayname"]').value;
		if (displayname.length > 0){
			document.querySelector('#newbtn').disabled = false;
		} else {
			document.querySelector('#newbtn').disabled = true;
		}


		//ajax request to check displayname availability
		const request = new XMLHttpRequest();
		request.open('POST', '/checkdispname');
		request.onload = () => {
			const response = JSON.parse(request.responseText);
			const msg = `${response.msg}`
			if (response.available) {
				document.querySelector('.validation').innerHTML = msg;
			} else {
				document.querySelector('.validation').innerHTML = msg;
				document.querySelector('#newbtn').disabled = true;
			}


		


		};

		//send the displayname  along with the request
		const data = new FormData();
		data.append('displayname', displayname);
		//send request

		request.send(data);

	};


});