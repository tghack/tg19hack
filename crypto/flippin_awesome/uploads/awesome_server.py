#!/usr/bin/env python2
from flask import Flask, render_template, request, url_for, redirect, make_response
import json
import sys
from base64 import b64decode, b64encode
from binascii import hexlify
from hashlib import md5
from Crypto.Cipher import AES
from Crypto import Random
import subprocess

app = Flask(__name__)
# Note: dummy key, production uses a secret random key
app.secret_key = '\x00' * 16

BLOCK_SIZE = 16
pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * \
                chr(BLOCK_SIZE - len(s) % BLOCK_SIZE)
unpad = lambda s: s[:-ord(s[len(s) - 1:])]


# https://gist.github.com/forkd/168c9d74b988391e702aac5f4aa69e41
class AESCipher:
    """
    Usage:
        c = AESCipher('password').encrypt('message')
        m = AESCipher('password').decrypt(c)
    Tested under Python 3 and PyCrypto 2.6.1.
    """

    def __init__(self, key):
        self.key = md5(key.encode('utf8')).hexdigest()

    def encrypt(self, raw):
        raw = pad(raw)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return b64encode(iv + cipher.encrypt(raw))

    def decrypt(self, enc):
        enc = b64decode(enc)
        iv = enc[:16]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return unpad(cipher.decrypt(enc[16:])).decode('utf8')


@app.route("/")
def main():
    return render_template('./login.html')


def sanitize_username(user):
    forbidden = ";&><|$()[]{}.,/\\=+-`~!@#%^"
    fixed = ""
    for c in user:
        if c in forbidden:
            fixed += ' '
        else:
            fixed += c
    return fixed


@app.route('/login', methods=['GET', 'POST'])
def login():
    resp = make_response(redirect("/motd"))

    cookie = {}
    cookie['username'] = sanitize_username(request.form['user'])
    cookie['cmd'] = 'echo \"Welcome, {}!\nHere\'s the time: $(date)\"'.format(cookie['username'])

    cookie_data = json.dumps(cookie, sort_keys=True)
    print(cookie_data)
    encrypted = AESCipher(app.secret_key).encrypt(cookie_data)

    resp.set_cookie('motd', encrypted)
    return resp


@app.route('/motd', methods=['GET'])
def motd():
    if "motd" not in request.cookies:
        return redirect(url_for("main"))
    encrypted = request.cookies["motd"]
    data = AESCipher(app.secret_key).decrypt(encrypted)
    data = json.loads(data)
    cmd = data["cmd"]

    # https://docs.python.org/3/library/subprocess.html#subprocess.check_output
    out = subprocess.check_output(cmd + "; exit 0", stderr=subprocess.STDOUT, shell=True)
    return render_template('motd.html', welcome=out.decode("utf-8"))


if __name__ == "__main__":
    app.run(debug=True)
