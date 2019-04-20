#!/usr/bin/env python3
import requests
import binascii

url="http://notc2.tghack.no/get_flag"
headers = {
    'User-Agent': 'secretstringkey'
}

data = requests.get(url, headers=headers)
flagenc=data.text.strip()
lol=binascii.unhexlify(flagenc)
key=len(lol)
flag=""

for c in lol:
    flag+=chr(c ^ key)

print(flag)
