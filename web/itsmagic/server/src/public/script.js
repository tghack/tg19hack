const rooturl = window.location.protocol+"//"+window.location.host+"/";

function init() {
	// Enable button click on enter

	// Get the input fields
	var usernameInput = document.getElementById("username");
	var passwordInput = document.getElementById("password");

	// Execute a function when the user releases a key on the keyboard
	usernameInput.addEventListener("keyup", function (event) {
		// Cancel the default action, if needed
		event.preventDefault();
		// Number 13 is the "Enter" key on the keyboard
		if (event.keyCode === 13) {
			// Trigger the button element with a click
			document.getElementById("myBtn").click();
		}
	});

	passwordInput.addEventListener("keyup", function (event) {
		// Cancel the default action, if needed
		event.preventDefault();
		// Number 13 is the "Enter" key on the keyboard
		if (event.keyCode === 13) {
			// Trigger the button element with a click
			document.getElementById("myBtn").click();
		}
	});
}

function login() {
	// Nothing interesting here, just trying to make task seem like 
	// it has a real login page in a hacky way
	var username = document.getElementById('username').value;

	var request = new XMLHttpRequest();
	request.open('GET', rooturl + 'login/' + username);

	request.onload = function () {
		var data = JSON.parse(this.response);
		const userid = data.userid;

		if (request.status == 200 && userid != null)
			window.location.href = rooturl + "home/" + userid;
	}

	request.send();
}

function home() {
	// Just selecting grades randomly to illustrate that each user 
	// has their own grades (giving the feel of a real website)

	var request = new XMLHttpRequest();
	request.open('GET', rooturl + 'userid/');
	var userid;

	request.onload = function () {
		var data = JSON.parse(this.response);
		userid = data.userid

		var grades = ['A', 'B', 'C', 'D', 'E', 'F'];

		var cryptograde = document.getElementById('cryptograde');
		var beastsgrade = document.getElementById('beastsgrade');
		var pwntionsgrade = document.getElementById('pwntionsgrade');
		var darkartsgrade = document.getElementById('darkartsgrade');
		var useridelement = document.getElementById('userid');

		cryptograde.innerText = grades[userid % grades.length];
		beastsgrade.innerText = grades[(userid + 5) % grades.length];
		pwntionsgrade.innerText = grades[(userid + 3) % grades.length];
		darkartsgrade.innerText = grades[(userid + 7) % grades.length];
		useridelement.innerText = 'Welcome, wizard/witch#' + userid;
	}

	request.send();
}
