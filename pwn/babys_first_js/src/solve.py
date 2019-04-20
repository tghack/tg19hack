from pwn import *
import sys

r = remote("js.tghack.no", 9001)
#r = remote("localhost", 9001)

r.recvline()

js_code = open(sys.argv[1], "r").read()
r.sendline(js_code + "\n" + "EOF")

r.interactive()
