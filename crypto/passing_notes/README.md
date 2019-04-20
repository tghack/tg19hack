# Passing notes
**Points: 150**

**Author: Chabz**

**Difficulty: challenging**

**Category: crypto**
___
In one of my classes, some students 
were sending notes back and forth. 
I confiscated one of the notes, but it
only contained this:
```
vyLlwWSY1PCK5ELNTPUVdpl8z0rIXiB2+Ybcu/BeXidR3MEiym852HCkS6wHVCr+CdpP6Moe9VQUeFcyq3vZDpVK/orl+8vREYMRrnQR9O4=
```
I got curious and decided to hack
into their server, but the only 
interesting information I could find
was this hash:
```
bbb2c5e63d2ef893106fdd0d797aa97a
```
and the following code:
```python
import base64
from Crypto.Cipher import AES
from Crypto import Random
from Crypto.Hash import SHA256
from struct import pack

BS = 16
secret = b'not_the_secret'
key = SHA256.new()
key.update(secret)

def encrypt(key, message):
    iv = Random.new().read(BS)
    pad_len = BS - divmod(len(message), BS)[1]
    padding = [pad_len]*pad_len
    padding = pack('b'*pad_len, *padding)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return base64.b64encode(iv + cipher.encrypt(message + padding))
```
But now I'm stuck. Think you can help me
out?

