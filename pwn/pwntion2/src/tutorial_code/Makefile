CC=gcc -m32
CFLAGS=-Wall -Wextra
CFLAGS+=-fno-stack-protector # disable stack cookies
CFLAGS+=-z execstack # disable NX
CFLAGS+=-no-pie # disable randomising of addresses
CFLAGS+=-Wl,-z,norelro # disable RELRO (GOT is writeable)
CFLAGS+=-g

.PHONY: all, run, clean
all: pwn_intro2

flip: pwn_intro2.c
	$(CC) $(CFLAGS) $^ -o $@

run: pwn_intro2
	./$^

clean:
	rm -vf pwn_intro2
