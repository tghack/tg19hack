# Piece of Pi writeup

We can start by connecting to the service to see what we're dealing with:

```
$ nc pi.tghack.no 2015
Give me data (pad to 1024 bytes):
```

Okay, so we need to send 1024 bytes of data to the service. Let's create a tiny
script that can do this for us using `pwntools`.


```python
from pwn import *
from StringIO import StringIO
from gzip import GzipFile

r = remote("pi.tghack.no", 2015)

r.recvuntil(": ")

buf = "\x00" * 1024
out = StringIO()
with GzipFile(fileobj=out, mode="w") as f:
	f.write(buf)

gz_data = out.getvalue()
r.send(gz_data + "\x00" * (1024 - len(gz_data)))

r.interactive()
```

We connect to the service, and then send 1024 zero bytes as gzipped data.

```
$ python2 solve.py
[+] Opening connection to pi.tghack.no on port 2015: Done
[*] Switching to interactive mode
[+] running command: ['./qemu/build/arm-softmmu/qemu-system-arm', '-M', 'raspi2', '-serial', 'stdio', '-kernel', '/tmp/tmpTx99En/loader.elf']
```

Interesting! The task description hints to the Raspberry Pi, but the command
run verifies this: `-M raspi2`. It seems like the service is starting qemu
with the data we gave it as the `-kernel` argument.

From the description, we know that we have to use UART to print the flag at
address `0x1337`. By googling a bit after bare metal programming for the
Raspberry Pi, you might find this tutorial: https://jsandler18.github.io/

The tutorial has instructions on how to create your own kernel for the
Raspberry Pi. One of the first things covered in the tutorial is how to write
to UART. We take the code and modify it so that everything is located in
one file, and only keep the functionality that we are interested in, which is
printing using UART. We also needed the early boot code.

kernel.c:
```C
#include <stddef.h>
#include <stdint.h>
 
// Memory-Mapped I/O output
static inline void mmio_write(uint32_t reg, uint32_t data)
{
	*(volatile uint32_t*)reg = data;
}
 
// Memory-Mapped I/O input
static inline uint32_t mmio_read(uint32_t reg)
{
	return *(volatile uint32_t*)reg;
}
 
// Loop <delay> times in a way that the compiler won't optimize away
static inline void delay(int32_t count)
{
	asm volatile("__delay_%=: subs %[count], %[count], #1; bne __delay_%=\n"
		 : "=r"(count): [count]"0"(count) : "cc");
}
 
enum
{
    // The GPIO registers base address.
    GPIO_BASE = 0x3F200000, // for raspi2 & 3, 0x20200000 for raspi1
 
    // The offsets for reach register.
 
    // Controls actuation of pull up/down to ALL GPIO pins.
    GPPUD = (GPIO_BASE + 0x94),
 
    // Controls actuation of pull up/down for specific GPIO pin.
    GPPUDCLK0 = (GPIO_BASE + 0x98),
 
    // The base address for UART.
    UART0_BASE = 0x3F201000, // for raspi2 & 3, 0x20201000 for raspi1
 
    // The offsets for reach register for the UART.
    UART0_DR     = (UART0_BASE + 0x00),
    UART0_RSRECR = (UART0_BASE + 0x04),
    UART0_FR     = (UART0_BASE + 0x18),
    UART0_ILPR   = (UART0_BASE + 0x20),
    UART0_IBRD   = (UART0_BASE + 0x24),
    UART0_FBRD   = (UART0_BASE + 0x28),
    UART0_LCRH   = (UART0_BASE + 0x2C),
    UART0_CR     = (UART0_BASE + 0x30),
    UART0_IFLS   = (UART0_BASE + 0x34),
    UART0_IMSC   = (UART0_BASE + 0x38),
    UART0_RIS    = (UART0_BASE + 0x3C),
    UART0_MIS    = (UART0_BASE + 0x40),
    UART0_ICR    = (UART0_BASE + 0x44),
    UART0_DMACR  = (UART0_BASE + 0x48),
    UART0_ITCR   = (UART0_BASE + 0x80),
    UART0_ITIP   = (UART0_BASE + 0x84),
    UART0_ITOP   = (UART0_BASE + 0x88),
    UART0_TDR    = (UART0_BASE + 0x8C),
};
 
void uart_init()
{
	// Disable UART0.
	mmio_write(UART0_CR, 0x00000000);
	// Setup the GPIO pin 14 && 15.
 
	// Disable pull up/down for all GPIO pins & delay for 150 cycles.
	mmio_write(GPPUD, 0x00000000);
	delay(150);
 
	// Disable pull up/down for pin 14,15 & delay for 150 cycles.
	mmio_write(GPPUDCLK0, (1 << 14) | (1 << 15));
	delay(150);
 
	// Write 0 to GPPUDCLK0 to make it take effect.
	mmio_write(GPPUDCLK0, 0x00000000);
 
	// Clear pending interrupts.
	mmio_write(UART0_ICR, 0x7FF);
 
	// Set integer & fractional part of baud rate.
	// Divider = UART_CLOCK/(16 * Baud)
	// Fraction part register = (Fractional part * 64) + 0.5
	// UART_CLOCK = 3000000; Baud = 115200.
 
	// Divider = 3000000 / (16 * 115200) = 1.627 = ~1.
	mmio_write(UART0_IBRD, 1);
	// Fractional part register = (.627 * 64) + 0.5 = 40.6 = ~40.
	mmio_write(UART0_FBRD, 40);
 
	// Enable FIFO & 8 bit data transmissio (1 stop bit, no parity).
	mmio_write(UART0_LCRH, (1 << 4) | (1 << 5) | (1 << 6));
 
	// Mask all interrupts.
	mmio_write(UART0_IMSC, (1 << 1) | (1 << 4) | (1 << 5) | (1 << 6) |
	                       (1 << 7) | (1 << 8) | (1 << 9) | (1 << 10));
 
	// Enable UART0, receive & transfer part of UART.
	mmio_write(UART0_CR, (1 << 0) | (1 << 8) | (1 << 9));
}
 
void uart_putc(unsigned char c)
{
	// Wait for UART to become ready to transmit.
	while ( mmio_read(UART0_FR) & (1 << 5) ) { }
	mmio_write(UART0_DR, c);
}
 
unsigned char uart_getc()
{
    // Wait for UART to have received something.
    while ( mmio_read(UART0_FR) & (1 << 4) ) { }
    return mmio_read(UART0_DR);
}
 
void uart_puts(const char* str)
{
	for (size_t i = 0; str[i] != '\0'; i ++)
		uart_putc((unsigned char)str[i]);
}
 
#if defined(__cplusplus)
extern "C" /* Use C linkage for kernel_main. */
#endif
void kernel_main(uint32_t r0, uint32_t r1, uint32_t atags)
{
	// Declare as unused
	(void)r0;
	(void)r1;
	(void)atags;
 
	uart_init();
	uart_puts("flag pls");
 
	while (1)
		uart_putc(uart_getc());
}
```

boot.S:
```asm
// To keep this in the first portion of the binary.
.section ".text.boot"
 
// Make _start global.
.globl _start
 
// Entry point for the kernel.
// r15 -> should begin execution at 0x8000.
// r0 -> 0x00000000
// r1 -> 0x00000C42
// r2 -> 0x00000100 - start of ATAGS
// preserve these registers as argument for kernel_main
_start:
	mrc	p15, #0, r1, c0, c0, #5
	and	r1, r1, #3
	cmp	r1, #0
	bne	halt
	// Setup the stack.
	mov sp, #0x8000
 
	// Clear out bss.
	ldr r4, =__bss_start
	ldr r9, =__bss_end
	mov r5, #0
	mov r6, #0
	mov r7, #0
	mov r8, #0
	b       2f
 
1:
	// store multiple at r4.
	stmia r4!, {r5-r8}
 
	// If we are still below bss_end, loop.
2:
	cmp r4, r9
	blo 1b
 
	// Call kernel_main
	mov	r2, #0x100
	ldr r3, =kernel_main
	blx r3
	b halt

 
	// halt
halt:
	wfe
	b halt
```

And here's the Makefile:
```
CC=arm-none-eabi-gcc
CFLAGS=-mcpu=cortex-a7 -fpic -ffreestanding

.PHONY: all run clean
all: kernel.img

boot.o: boot.S
	$(CC) $(CFLAGS) -c $^ -o $@

kernel.o: kernel.c
	$(CC) $(CFLAGS) -std=gnu99 -c $^ -o $@ -O2 -Wall -Wextra

kernel.elf: boot.o kernel.o
	$(CC) -T linker.ld -o kernel.elf -ffreestanding -O2 -nostdlib $^

run: kernel.elf
	qemu-system-arm -bios bios.bin -m 256 -M raspi2 -serial stdio -kernel $^

clean:
	rm -f kernel.elf *.o
```

And finally, the linker script (linker.ld):
```
ENTRY(_start)
 
SECTIONS
{
    /* Starts at LOADER_ADDR. */
    . = 0x8000;
    __start = .;
    __text_start = .;
    .text :
    {
        KEEP(*(.text.boot))
        *(.text)
    }
    . = ALIGN(4096); /* align to page size */
    __text_end = .;
 
    __rodata_start = .;
    .rodata :
    {
        *(.rodata)
    }
    . = ALIGN(4096); /* align to page size */
    __rodata_end = .;
 
    __data_start = .;
    .data :
    {
        *(.data)
    }
    . = ALIGN(4096); /* align to page size */
    __data_end = .;
 
    __bss_start = .;
    .bss :
    {
        bss = .;
        *(.bss)
    }
    . = ALIGN(4096); /* align to page size */
    __bss_end = .;
    __end = .;
}
```

Running `make run` should print `flag pls` in your terminal. Let's send it to
the server and see if it works!

```
$ python2 solve.py
[+] Opening connection to pi.tghack.no on port 2015: Done
[*] Switching to interactive mode
[+] running command: ['./qemu/build/arm-softmmu/qemu-system-arm', '-M', 'raspi2', '-serial', 'stdio', '-kernel', '/tmp/tmp8itpIL/loader.elf']
flag pls
```

Nice! The only thing left to do is to add some code that prints the flag at
`0x1337`.

```C
char *addr = (char *)0x1337;
uart_puts(addr);
```

```
python2 solve.py
[+] Opening connection to pi.tghack.no on port 2015: Done
[*] Switching to interactive mode
[+] running command: ['./qemu/build/arm-softmmu/qemu-system-arm', '-M', 'raspi2', '-serial', 'stdio', '-kernel', '/tmp/tmpqgTAps/loader.elf']
flag pls
TG19{tiny_raspberry_pi_kernels_everywhere}
```
