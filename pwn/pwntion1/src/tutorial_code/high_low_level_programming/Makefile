CC=gcc -m32
CFLAGS=-Wall -Wextra
CFLAGS+=-fno-stack-protector # disable stack cookies
CFLAGS+=-z execstack # disable NX
CFLAGS+=-no-pie # disable randomising of addresses
CFLAGS+=-z,norelro # disable RELRO (GOT is writeable)
CFLAGS+=-g

.PHONY: all, run, clean
all: low_level_ex

flip: low_level_ex.c
	$(CC) $(CFLAGS) $^ -o $@

run: low_level_ex
	./$^

public: low_level_ex_public.c
	$(CC) $(CFLAGS) $^ -o low_level_ex_$@

clean:
	rm -vf low_level_ex
