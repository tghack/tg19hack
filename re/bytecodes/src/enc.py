#!/usr/bin/env python3
import binascii

flag = "TG19{python_bytecode_in_the_house}"

key = 0x42


enc = "".join([chr(ord(c) ^ key) for c in flag])
enc = enc.encode("utf-8")
print(binascii.hexlify(enc))
