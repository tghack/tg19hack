CC=gcc -m32
CFLAGS=-Wall -Wextra
CFLAGS+=-fno-stack-protector # disable stack cookies
CFLAGS+=-z execstack # disable NX
CFLAGS+=-no-pie # disable randomising of addresses
CFLAGS+=-Wl,-z,norelro # disable RELRO (GOT is writeable)
CFLAGS+=-g

.PHONY: all, run, clean
all: pwntion2

flip: pwntion2.c
	$(CC) $(CFLAGS) $^ -o $@

run: pwntion2
	./$^

clean:
	rm -vf pwntion2
