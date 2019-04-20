#!/usr/bin/env python2
from pwn import *
from StringIO import StringIO
from gzip import GzipFile

r = remote("pi.tghack.no", 2015)

with open("kernel/kernel.elf", "rb") as f:
    data = f.read()

r.recvuntil(": ")

out = StringIO()
with GzipFile(fileobj=out, mode="w") as f:
    f.write(data)

gz_data = out.getvalue()
r.send(gz_data + "\x00" * (1024 - len(gz_data)))

r.interactive()
