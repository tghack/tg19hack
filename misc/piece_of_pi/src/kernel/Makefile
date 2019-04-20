CC=arm-none-eabi-gcc
CFLAGS=-mcpu=cortex-a7 -fpic -ffreestanding

.PHONY: all run clean
all: kernel.elf

boot.o: boot.S
	$(CC) $(CFLAGS) -c $^ -o $@

kernel.o: kernel.c
	$(CC) $(CFLAGS) -std=gnu99 -c $^ -o $@ -O2 -Wall -Wextra

kernel.elf: boot.o kernel.o
	$(CC) -T linker.ld -o kernel.elf -ffreestanding -O2 -nostdlib $^

run: kernel.elf
	qemu-system-arm -m 256 -M raspi2 -serial stdio -kernel $^

clean:
	rm -f kernel.elf *.o
