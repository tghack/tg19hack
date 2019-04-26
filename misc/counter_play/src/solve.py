#!/usr/bin/env python
import sys
from pwn import *

REMOTE = True
suspicious_chars = '# & 0 4 6 9 8 A B D O Q P R a b e d g o q p'.split(' ')

if REMOTE:
    r = remote('counter.tghack.no', 2018)
    _ = r.recvuntil("text:\n\n")
    text = r.recvall()
    r.close()
else:
    with open('flag.enc', 'r') as f:
        text = f.read()

for ch in text:
    if ch == '\n':
        sys.stdout.write('\n')
    elif ch in suspicious_chars:
        sys.stdout.write(ch)
    else:
        sys.stdout.write(' ')
