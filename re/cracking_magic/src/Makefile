CC=gcc
CFLAGS=-Wall -Wextra

.PHONY: all clean

all: key_check.elf

key_check.elf: key_check.c
	$(CC) $(CFLAGS) $^ -o $@
	strip $@

clean:
	rm -f key_check.elf
