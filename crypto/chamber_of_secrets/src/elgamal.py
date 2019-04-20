from sage.all import *
from Crypto.Cipher import Blowfish
from Crypto import Random

flag = "TG19{please_be_more_discreet_when_hacking}"

q = (2**50)-27
print(q)

b = -3
print(b)

c = 0x64210519e59c80e70fa7e9ab72243049feb8deecc146b9b1
c = c%q
print(c)

E = EllipticCurve(GF(q), [b,c])
print(E)

g = E.random_point()
print(g)

x = ZZ.random_element(q)
print(x)

h = g*x
print(h)

# public(h, E, q, g)
# private(x)

def encrypt(m):
    y = ZZ.random_element(q)
    c1 = g*y
    s = h*y
    c2 = m+s
    return (c1, c2)

def decrypt((c1, c2)):
    s = c1*x
    m = c2-s
    return m

m = E.random_point()
print(m)

c = encrypt(m)
print(c)

m1 = decrypt(c)
print(m1)

def crack((c1, c2)):
    discLog = g.discrete_log(h)
    s = c1*discLog
    m = c2-s
    return m

cracked = crack(c)
print(cracked)

