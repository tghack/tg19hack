# Writeup [Passing notes](README.md)
**Points: 150**

**Author: Chabz**

**Difficulty: challenging**

**Category: crypto**
___
In this task we are given some 
encrypted text, together with 
the encryption function and a 
hash. Looking at the function, we
see it's using AES. It also looks
like a normal usage of AES, so we 
will leave it alone for now. Let's 
have a look at the hash instead.

Hash algorithms always have fixed
length on the output, so we can check
the length of the hash:
```python
$ python
Python 3.7.3 (default, Mar 26 2019, 21:43:19) 
[GCC 8.2.1 20181127] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> len("bbb2c5e63d2ef893106fdd0d797aa97a")
32
```
This hash is 32 bytes long (128 bits).
Looking at [this Wikipedia page](https://en.wikipedia.org/wiki/Secure_Hash_Algorithms),
we see that MD5 has this output size.
[MD5](https://en.wikipedia.org/wiki/MD5)
is also known to be insecure for password 
hashing. There are many websites where
you can look up MD5 hashes, one of them
being [CrackStation](https://crackstation.net/).
Pasting in the hash gives us this secret:
```
supersecretpassword
```
Nice, now we just need to code a decrypt
function:
```python
import base64
from Crypto.Cipher import AES
from Crypto.Hash import SHA256

secret = b'supersecretpassword'
key = SHA256.new()
key.update(secret)

def decrypt(key, enc):
    enc = base64.b64decode(enc)
    iv = enc[:16]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return cipher.decrypt(enc[16:])

denc = decrypt(key.digest(), b'vyLlwWSY1PCK5ELNTPUVdpl8z0rIXiB2+Ybcu/BeXidR3MEiym852HCkS6wHVCr+CdpP6Moe9VQUeFcyq3vZDpVK/orl+8vREYMRrnQR9O4=')
print(denc)
```
Running it gives us the flag:
```
$ python solve.py
b'TG19{you_should_really_consider_updating_your_hash_algorithm}\x03\x03\x03'
```
