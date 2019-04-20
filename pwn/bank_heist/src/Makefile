kvm: kvm.c bank.h
	gcc -Wall -Wextra -o kvm kvm.c
bank.h: bank
	xxd -i bank > bank.h

bank: bank.c
	gcc -std=gnu99 -Os -nostdlib -m16 -march=i386 -fno-pie -ffreestanding -o bank -Wl,--nmagic,--script=script.ld bank.c
	gcc -std=gnu99 -Os -nostdlib -m16 -march=i386 -fno-pie -ffreestanding -o elfbank -Wl,--nmagic,--script=elf_script.ld bank.c

shellcode: shellcode.s
	gcc -m16 shellcode.s -Telf_script.ld -nostdlib -o shellcode && objdump -mi386 -Maddr16,data16 -z -d shellcode
	objdump -z -d shellcode|grep '[0-9a-f]:'|grep -v 'file'|cut -f2 -d:|cut -f1-6 -d' '|tr '\n' ' '| tr '\t' ' '|tr -s ' '|sed 's/ $$//g'|sed 's/ /\\x/g'

.PHONY: shellcode
