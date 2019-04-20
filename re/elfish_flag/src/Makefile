CC=gcc
CFLAGS=-Wall -Wextra

.PHONY: all clean

all: elfish.elf

elfish.elf: main.c
	$(CC) $(CFLAGS) $^ -o $@
	strip $@

clean:
	rm -f elfish.elf
