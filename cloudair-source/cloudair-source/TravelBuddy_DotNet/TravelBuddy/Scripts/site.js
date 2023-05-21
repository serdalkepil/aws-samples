$('.flighttime').each(function() {  
	calculate($(this));         
});

function calculate($currentElement) {
	
	var dateFuture = new Date($currentElement.data("expiry"));
	var dateNow = new Date();

	var seconds = Math.floor((dateFuture - (dateNow))/1000);
	var minutes = Math.floor(seconds/60);
	var hours = Math.floor(minutes/60);
	var days = Math.floor(hours/24);

	hours = hours-(days*24);
	minutes = minutes-(days*24*60)-(hours*60);
	seconds = seconds-(days*24*60*60)-(hours*60*60)-(minutes*60);
	
	var message = "";
	if ( days > 30 )
		message = "Plenty of time";
	else if ( days > 1 )
		message = days + " days to go";
	else if ( hours > 1 )
		message = hours + " hours to go";
	else if ( minutes > 30 )
		message = minutes + " minutes to go";
	else 
		{
			if ( minutes == 1)
				message = "1 minute to go";
			else if ( minutes <= 0 )
				message = "deal over";
			else
				message = minutes + " minutes to go";
				
			$currentElement.addClass("flighttime-urgent");
		}
	
	$currentElement.text(message);
}