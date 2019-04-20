const express = require('express');
const fs = require('fs');
const path = require('path');
const IMAGE = fs.readFileSync('./fortune.jpg');
const PORT = 50501;
const GUEST_TOKEN = "access_token=divination:student"
const ADMIN_TOKEN = "access_token=divination:professor"

var app = express();
var accessToken = GUEST_TOKEN

app.use(express.static('public'));

app.get('/', (req, res) => {
	var cookie = req.headers.cookie
	var cookieArray = cookie != null ? cookie.split(";") : ""
	
	// If cookies are cleared in browser
	if (cookieArray == "") {
		accessToken = GUEST_TOKEN 
	}

	// Fetch access_token from cookie
	for (x in cookieArray) {
		if (cookieArray[x].includes("access_token")) {
			accessToken = cookieArray[x]
			break;
		}
	}

	// Give flag if right cookie
	if (accessToken.includes(ADMIN_TOKEN)) {
		res.status(200).send("OMG! You're so fortunate! Take this flag: TG19{what_a_fortune_my_lucky_one}");
		return;
	}

    res.append('Set-Cookie', accessToken);
    res.sendFile(path.join(__dirname, 'index.html'));
});

app.get('/fortune.jpg', (req, res) => {
	res.send(IMAGE);
});

app.listen(PORT);
