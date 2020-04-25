$(document).ready(function() {
	$( ".card" ).hover(
		function() {
			// $(this).addClass('shadow');.css('cursor', 'pointer'); 
			$(this).addClass('shadow');
		},
		function() {
			$(this).removeClass('shadow');
		}
	);
});
