window.setInterval(function(){ // Set interval for checking
	var date = new Date(); // Create a Date object to find out what time it is
	if(date.getHours() === 20 && date.getMinutes() === 6){ // Check the time
		alert("Current time is - 20:06");
	}
}, 60000); // Repeat every 60000 milliseconds (1 minute)