#CC=gcc
CC=clang
CFLAGS=-Wall -Wextra -fstack-protector-strong -D_FORTIFY_SOURCE=2

.PHONY: all, run, clean
all: flip

flip: flip.c
	$(CC) $(CFLAGS) $^ -o $@

run: flip
	./$^

clean:
	rm -vf flip
