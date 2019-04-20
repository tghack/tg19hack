# The Chamber of Secrets - Writeup
**Points: 300**

**Author: Chabz**

**Difficulty: hard**

**Category: crypto**
___

In this task, we are given some numbers and some python-code.
Let's take a look at the code first:
```python
key =  SHA256.new()
key.update(secret)

def bf_encrypt(key, message):
    bs = Blowfish.block_size
    iv = Random.new().read(bs)
    cipher = Blowfish.new(key, Blowfish.MODE_CBC, iv)
    pad_len = bs - divmod(len(message), bs)[1]
    padding = [pad_len]*pad_len
    padding = pack('b'*pad_len, *padding)
    return base64.b64encode(iv + cipher.encrypt(message + padding))
```
This looks like normal encryption using 
[Blowfish](https://www.dlitz.net/software/pycrypto/api/current/Crypto.Cipher.Blowfish-module.html).
It is using the SHA256 hash of a secret as key.
Our task must then be to find that secret. 

We are given the following data:
```
public(h, a, b, q, g)
h = (829999038570486 : 549144410878897 : 1)
a = -3
b = 313205882961673
q = 1125899906842597
g = (1115545019992514 : 78178829836422 : 1)
c = ((700253548714057 : 421820716153583 : 1), (470712751668926 : 131989609316847 : 1))

sTokhflo9WHPQB8JHEm0OVG2SwUA/sHaP0yFv9T2kmoZjC5g46eeRM8M8CGRj8bV/NxY4VJ8Ls0=
```
The last line looks like base64, but trying to
decode it gives us some garbage data. This is 
probably the encrypted data. The first line tells
us that we have a public key for some kind of 
asymmetric cipher. But which one? We can start
by looking up some of the more well known asymmetric
ciphers. For RSA and Diffie-Hellman, we see that 
public key we are given does not fit. But one that
looks promising, is [ElGamal](https://en.wikipedia.org/wiki/ElGamal_encryption).
Normal ElGamal uses a public key consisting of 
`h, G, q, g`. In our data, we have `h, q, g`, but we
have `a, b` instead of `G`. We also notice that
`h, g` are given as points, not single values. 
Could this be some kind of elliptic curve variant
of ElGamal? Looking up [ECC](https://en.wikipedia.org/wiki/Elliptic-curve_cryptography)
all but confirms our suspicion: `a, b` are parameters
used for creating elliptic curves. Oh well, time
to bring out the old [sage](http://www.sagemath.org/)!
```python
$ sage
┌────────────────────────────────────────────────────────────────────┐
│ SageMath version 8.6, Release Date: 2019-01-15                     │
│ Using Python 2.7.15. Type "help()" for help.                       │
└────────────────────────────────────────────────────────────────────┘
sage: a = -3
sage: b = 313205882961673
sage: q = 1125899906842597
sage: E = EllipticCurve(GF(q), [a, b])
sage: E
Elliptic Curve defined by y^2 = x^3 + 1125899906842594*x + 313205882961673 over Finite Field of size 1125899906842597
sage: h = E(829999038570486, 549144410878897)
sage: g = E(1115545019992514, 78178829836422)
sage: c = (E(700253548714057, 421820716153583), E(470712751668926, 131989609316847))
```
Now we have our elliptic curve. But what to do with it?
The size of the parameters suggest that it might
be possible to calculate the discrete logarithm
and decrypt the data. `sage` has a handy method we can
try:
```python
sage: discLog = g.discrete_log(h)
sage: discLog
29131765433887
```
Success! We can now use this value to compute the
secret from `c`:
```python
sage: s = c[0]*discLog
sage: m = c[1]-s
sage: m
(934013602642177 : 28034533961304 : 1)
```
We have our secret! Let's throw together some python code:
```python
import base64
from Crypto.Cipher import Blowfish
from Crypto.Hash import SHA256

ciphertext = "sTokhflo9WHPQB8JHEm0OVG2SwUA/sHaP0yFv9T2kmoZjC5g46eeRM8M8CGRj8bV/NxY4VJ8Ls0="
secret = b'934013602642177'
key =  SHA256.new()
key.update(secret)

def bf_decrypt(key, ciphertext):
    ciphertext = base64.b64decode(ciphertext)
    bs = Blowfish.block_size
    iv = ciphertext[:bs]
    cipher = Blowfish.new(key, Blowfish.MODE_CBC, iv)
    return cipher.decrypt(ciphertext)

print(bf_decrypt(key.digest(), ciphertext))
```
```bash
$ python writeup.py
b'P)y\xa5\xe6R\x13lTG19{please_be_more_discreet_when_hacking}\x06\x06\x06\x06\x06\x06'
```
(The random data comes from the padding in the encryption.)

