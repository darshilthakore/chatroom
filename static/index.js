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

		const request = new XMLHttpRequest();
		request.open('POST', '/checkdispname');
		request.onload = () => {
			const response = JSON.parse(request.responseText);

			if (response.available) {
				document.querySelector('.validation').innerHTML = "username available";
			} else {
				document.querySelector('.validation').innerHTML = "username not available";
				document.querySelector('#newbtn').disabled = true;
			}


			// document.querySelector('.validation').innerHTML= response;
			// document.querySelector('[name="newbtn"]').disabled = response.status;


		};

		//send the displayname  along with the request
		const data = new FormData();
		data.append('displayname', displayname);
		//send request

		request.send(data);

	};
	// function run(contents) {
	// 	document.querySelector('.validation').innerHTML = contents;
	// };


	
	// function checkdispname() {
	// 	const displayname = document.querySelector('[name="displayname"]').value;
		
	// };




});