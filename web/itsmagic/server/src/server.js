const express = require('express')
const path = require('path')
const app = express()
var USER_ID = require('./constants').USER_ID

var port = 2020;

app.get('/', (req, res) => res.sendFile(path.join(__dirname+'/index.html')))

app.get('/login/:username', (req, res) => {
	res.status(200).send({ 'userid': 1338 });
});

app.get('/home/:userid', (req, res) => {
	const userid = req.params.userid;

	if (isNaN(userid)){
		res.status(200).send("Oops, something went wrong.. Try something else.");
	}

	USER_ID = userid;

	if (userid == 1337)
		res.status(200).send("Congrats, y0ur s0 1337! </br>TG19{Direct object reference might B insecure!}");
	else
		res.sendFile(path.join(__dirname+'/public/home.html'))
});

app.get('/userid', (req, res) => {
	res.status(200).send({ 'userid': USER_ID });
});

app.use(express.static('public'));
app.listen(port, () => console.log('Magical app listening on port ' + port))
