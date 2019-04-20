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
