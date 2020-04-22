
// Change the type of input to password or text
function toggle_pass()
{
	var temp = document.getElementById("pwd1");
	if (temp.type === "password")
	{
		temp.type = "text";
	}
	else
	{
		temp.type = "password";
	}
}

function toggle_confirm()
{
	var temp = document.getElementById("pwd2");
	if (temp.type === "password")
	{
		temp.type = "text";
	}
	else
	{
		temp.type = "password";
	}
}
