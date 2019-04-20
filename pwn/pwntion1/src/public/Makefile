CC=gcc -m32
#CC=clang -m32 # noen ganger putter gcc inn shit på stacken
CFLAGS=-Wall -Wextra
CFLAGS+=-fno-stack-protector # skru av stack cookies
CFLAGS+=-z execstack # skru av NX
CFLAGS+=-no-pie # ikke randomiser addressen til binærfilen fno-pie
CFLAGS+=-Wl,-z,norelro # skru av RELRO (GOT er skrivbar)
CFLAGS+=-g

.PHONY: all, run, clean
all: pwntion1_public

flip: pwntion1_public.c
	$(CC) $(CFLAGS) $^ -o $@

run: pwntion1_public
	./$^

clean:
	rm -vf pwntion1_public
