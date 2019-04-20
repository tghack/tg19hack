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
