CC=gcc -m32
CFLAGS=-Wall -Wextra
CFLAGS+=-fno-stack-protector # disable stack cookies
CFLAGS+=-z execstack # disable NX
CFLAGS+=-no-pie # disable randomising of addresses
CFLAGS+=-Wl,-z,norelro # disable RELRO (GOT is writeable)
CFLAGS+=-g

.PHONY: all, run, clean
all: pwntion1

flip: pwntion1.c
	$(CC) $(CFLAGS) $^ -o $@

run: pwntion1
	./$^

public: pwntion1_public.c
	$(CC) $(CFLAGS) $^ -o pwntion1_$@

clean:
	rm -vf pwntion1
