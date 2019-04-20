const express = require('express');
const path = require('path');
const bodyParser = require('body-parser');
const sqlite3 = require('sqlite3');
const PORT = 4001;

var app = express();
app.use(bodyParser());
app.use(express.static('src'));
app.use(express.static('dist'))
app.use(express.static('lib'))

app.get('/health', (req, res) => {
	res.send("Magical app running!")
})

app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'index.html'))
})

app.post('/wand', (req, res) => {
	let body = req.body
	let id = body.id
	const query = `SELECT * FROM wands WHERE id = ${id}`

	let db = new sqlite3.Database('/home/node/database/wands.db', (err) => {
		if (err)
			console.error(err.message)

		console.log('Connected to DB!')
	}) 

	db.all(query, (err, result) => {
		if (err) {
			console.error(err.message)
			res.status(500).send({ 'message': err.message })
			return
		}

		if (result.length < 1) {
			res.status(500).send({ 'message': '500: Internal server error' })
			return
		}

		res.status(200).send({ result })
	})

	db.close((err) => {
		if (err) 
			console.error(err.message)

		console.log('Closed database connection.')
	})
})

app.listen(PORT, () => console.log('Magical app listening on port ' + PORT))

