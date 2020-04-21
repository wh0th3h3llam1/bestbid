function checkBidPrice()
{
	var baseprice = $('#baseprice').val();
	var bid_value = $('#bid_value').val();
	console.log(baseprice);
	console.log(bid_value);

	if(bid_value > baseprice)
	{
		console.log("Bid Value is greater than Base Price");
		// $('#bid_btn').removeAttr('disabled');
		$('#bid_btn').prop('disabled', false);
	}
	else
	{
		$('#bid_btn').prop('disabled', true);

	}
}