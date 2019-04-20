import sqlite3

from flask import Flask, render_template_string, request, redirect, make_response
import time

app = Flask(__name__)
app.debug = False

DB_NAME = "/tmp/wizardschat.db"

conn = sqlite3.connect(":memory:", check_same_thread = False)
conn.execute(
    "CREATE TABLE IF NOT EXISTS messages (author text, message text, timestamp integer);")

login_template = """
<html>
<head>
<title>WizardsChat</title>
<body>
<h1>Login</h1>
<div>
    <strong>Muggles no access! Use your magic to login</strong>
</div>
<form method="POST" action="/login">
<input type="hidden" name="has_magic" value="0" />
Username: <input type="text" name="username" /><br />
<input type="submit" value="Login" />
</form>
</body>
</html>
"""

muggle_template = """
<html>
<head>
<title>WizardsChat</title>
<body>
<h1>NO MAGIC DETECTED</h1>
</body>
</html>
"""

chat_template = """
<html>
<head>
    <title>WizardsChat</title>
<body>
<div>
    Username: {{username}}
</div>
<div>
    <h3>Send message</h3>
    <form method="POST" action="/send">
    <textarea rows="5" cols="80" name="text"></textarea><br />
    <input type="submit" value="Send!" />
    </form>
</div>
<hr />
<div>
    {% for msg in messages %}
    <div>{{msg.author}}: {{msg.text}}</div>
    {% endfor %}
</body>
</html>
"""


@app.route("/muggle", methods=['GET'])
def muggle():
    return render_template_string(muggle_template)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == "GET":
        return render_template_string(login_template)
    elif request.method == "POST":
        if request.form['has_magic'] != "1":
            return redirect("/muggle")
        resp = make_response(redirect("/"))
        resp.set_cookie('username', request.form['username'])
        return resp


@app.route("/send", methods=['POST'])
def send_msg():
    username = request.cookies['username'] or ''
    username = username.strip()
    if not username or len(username) == 0:
        return redirect("/login")

    msg = request.form['text'].strip()
    if not msg or len(msg) == 0:
        return redirect("/")

    cursor = conn.cursor()
    cursor.execute("INSERT INTO messages(author, message, timestamp) VALUES (?, ?, ?)",
                   (username, msg, int(time.time())))
    conn.commit()
    return redirect("/")


@app.route("/", methods=['GET', 'POST'])
def hello():
    username = request.cookies.get('username', default='')
    username = username.strip()
    if not username or len(username) == 0:
        return redirect("/login")
    messages = map(lambda x: {"author": x[0], "text": x[1]},
                   conn.execute("SELECT * FROM messages ORDER BY timestamp DESC LIMIT 5"))
    return render_template_string(chat_template.replace("{{username}}", username), messages=messages)
