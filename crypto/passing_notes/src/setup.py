import base64
from Crypto.Cipher import AES
from Crypto import Random
from Crypto.Hash import SHA256
from struct import pack

BS = 16

def encrypt(key, message):
    iv = Random.new().read(BS)
    pad_len = BS - divmod(len(message), BS)[1]
    padding = [pad_len]*pad_len
    padding = pack('b'*pad_len, *padding)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return base64.b64encode(iv + cipher.encrypt(message + padding))

def decrypt(key, enc):
    enc = base64.b64decode(enc)
    iv = enc[:16]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return cipher.decrypt(enc[16:])


flag = b'TG19{you_should_really_consider_updating_your_hash_algorithm}'
secret = b'supersecretpassword'
key = SHA256.new()
key.update(secret)

enc = encrypt(key.digest(), flag)
print(enc)

denc = decrypt(key.digest(), enc)
print(denc)


