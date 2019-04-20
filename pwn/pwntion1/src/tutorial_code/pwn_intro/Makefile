CC=gcc -m32
CFLAGS=-Wall -Wextra
CFLAGS+=-fno-stack-protector # disable stack cookies
CFLAGS+=-z execstack # disable NX
CFLAGS+=-no-pie # disable randomising of addresses
CFLAGS+=-z,norelro # disable RELRO (GOT is writeable)
CFLAGS+=-g

.PHONY: all, run, clean
all: pwn_intro1

flip: pwn_intro1.c
	$(CC) $(CFLAGS) $^ -o $@

run: pwn_intro1
	./$^

public: pwn_intro1_public.c
	$(CC) $(CFLAGS) $^ -o pwn_intro1_$@

clean:
	rm -vf pwn_intro1
