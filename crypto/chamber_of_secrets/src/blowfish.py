import base64
from Crypto.Cipher import Blowfish
from Crypto.Hash import SHA256
from Crypto import Random
from struct import pack

flag = b'TG19{please_be_more_discreet_when_hacking}'
secret = b'934013602642177'
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

def bf_decrypt(key, ciphertext):
    ciphertext = base64.b64decode(ciphertext)
    bs = Blowfish.block_size
    iv = ciphertext[:bs]
    cipher = Blowfish.new(key, Blowfish.MODE_CBC, iv)
    return cipher.decrypt(ciphertext)


ciphertext = bf_encrypt(key.digest(), flag)
print(ciphertext)
cleartext = bf_decrypt(key.digest(), ciphertext)
print(cleartext)
