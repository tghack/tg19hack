# Cracking Magic writeup
**Points: 250**

**Author: PewZ**

**Difficulty: challenging**

**Category: reversing**

---

Let's take a quick look at the binary in radare2:
```bash
[0x00000880]> pdf @ main
/ (fcn) main 249
|   main ();
|           ; var int local_30h @ rbp-0x30
|           ; var int local_28h @ rbp-0x28
|           ; var int local_20h @ rbp-0x20
|           ; var int local_18h @ rbp-0x18
|           ; var int local_8h @ rbp-0x8
|              ; DATA XREF from 0x0000089d (entry0)
|           0x00000b30      55             push rbp
|           0x00000b31      4889e5         mov rbp, rsp
|           0x00000b34      4883ec30       sub rsp, 0x30               ; '0'
|           0x00000b38      64488b042528.  mov rax, qword fs:[0x28]    ; [0x28:8]=0x2128 ; '('
|           0x00000b41      488945f8       mov qword [local_8h], rax
|           0x00000b45      31c0           xor eax, eax
|           0x00000b47      48c745d00000.  mov qword [local_30h], 0
|           0x00000b4f      48c745d80000.  mov qword [local_28h], 0
|           0x00000b57      48c745e00000.  mov qword [local_20h], 0
|           0x00000b5f      66c745e80000   mov word [local_18h], 0
|           0x00000b65      488b05a41420.  mov rax, qword [obj.stdout] ; [0x202010:8]=0
|           0x00000b6c      b900000000     mov ecx, 0
|           0x00000b71      ba02000000     mov edx, 2
|           0x00000b76      be00000000     mov esi, 0
|           0x00000b7b      4889c7         mov rdi, rax
|           0x00000b7e      e8adfcffff     call sym.imp.setvbuf        ; int setvbuf(FILE*stream, char*buf, int mode, size_t size)
|           0x00000b83      488d3d2a0100.  lea rdi, qword str.Serial_please: ; 0xcb4 ; "Serial please: "
|           0x00000b8a      b800000000     mov eax, 0
|           0x00000b8f      e86cfcffff     call sym.imp.printf         ; int printf(const char *format)
|           0x00000b94      488b15851420.  mov rdx, qword [obj.stdin]  ; [0x202020:8]=0
|           0x00000b9b      488d45d0       lea rax, qword [local_30h]
|           0x00000b9f      be1a000000     mov esi, 0x1a
|           0x00000ba4      4889c7         mov rdi, rax
|           0x00000ba7      e874fcffff     call sym.imp.fgets          ; char *fgets(char *s, int size, FILE *stream)
|           0x00000bac      4885c0         test rax, rax
|       ,=< 0x00000baf      7516           jne 0xbc7
|       |   0x00000bb1      488d3d0c0100.  lea rdi, qword str.fgets    ; 0xcc4 ; "fgets()"
|       |   0x00000bb8      e883fcffff     call sym.imp.perror         ; void perror(const char *s)
|       |   0x00000bbd      bf01000000     mov edi, 1
|       |   0x00000bc2      e889fcffff     call sym.imp.exit           ; void exit(int status)
|       `-> 0x00000bc7      488d45d0       lea rax, qword [local_30h]
|           0x00000bcb      488d35fa0000.  lea rsi, qword [0x00000ccc] ; "\n"
|           0x00000bd2      4889c7         mov rdi, rax
|           0x00000bd5      e836fcffff     call sym.imp.strcspn        ; size_t strcspn(const char *s1, const char *s2)
|           0x00000bda      c64405d000     mov byte [rbp + rax - 0x30], 0
|           0x00000bdf      488d45d0       lea rax, qword [local_30h]
|           0x00000be3      4889c7         mov rdi, rax
|           0x00000be6      e84bfeffff     call fcn.00000a36
|           0x00000beb      85c0           test eax, eax
|       ,=< 0x00000bed      7413           je 0xc02
|       |   0x00000bef      488d3dd80000.  lea rdi, qword str.yay      ; 0xcce ; "yay!"
|       |   0x00000bf6      e8d5fbffff     call sym.imp.puts           ; int puts(const char *s)
|       |   0x00000bfb      b800000000     mov eax, 0
|      ,==< 0x00000c00      eb11           jmp 0xc13
|      |`-> 0x00000c02      488d3dca0000.  lea rdi, qword str.nay      ; 0xcd3 ; "nay!"
|      |    0x00000c09      e8c2fbffff     call sym.imp.puts           ; int puts(const char *s)
|      |    0x00000c0e      b801000000     mov eax, 1
|      |       ; JMP XREF from 0x00000c00 (main)
|      `--> 0x00000c13      488b4df8       mov rcx, qword [local_8h]
|           0x00000c17      6448330c2528.  xor rcx, qword fs:[0x28]
|       ,=< 0x00000c20      7405           je 0xc27
|       |   0x00000c22      e8c9fbffff     call sym.imp.__stack_chk_fail ; void __stack_chk_fail(void)
|       `-> 0x00000c27      c9             leave
\           0x00000c28      c3             ret
```

We see that the last function called in `main()` before the program either
prints "yay!" or "nay!" is `fcn.00000a36`. This is probably the key checking
function, so let's take a look!


```bash
[0x00000880]> pdf @ fcn.00000a36
            ;-- rip:
/ (fcn) fcn.00000a36 250
|   fcn.00000a36 ();
|           ; var int local_28h @ rbp-0x28
|           ; var int local_18h @ rbp-0x18
|           ; var int local_10h @ rbp-0x10
|           ; var int local_8h @ rbp-0x8
|              ; CALL XREF from 0x00000be6 (main)
|           0x00000a36      55             push rbp
|           0x00000a37      4889e5         mov rbp, rsp
|           0x00000a3a      4883ec30       sub rsp, 0x30               ; '0'
|           0x00000a3e      48897dd8       mov qword [local_28h], rdi
|           0x00000a42      488b45d8       mov rax, qword [local_28h]
|           0x00000a46      4889c7         mov rdi, rax
|           0x00000a49      e892fdffff     call sym.imp.strlen         ; size_t strlen(const char *s)
|           0x00000a4e      488945f8       mov qword [local_8h], rax
|           0x00000a52      48837df818     cmp qword [local_8h], 0x18  ; [1]
|       ,=< 0x00000a57      740a           je 0xa63
|       |   0x00000a59      b800000000     mov eax, 0
|      ,==< 0x00000a5e      e9cb000000     jmp 0xb2e
|      |`-> 0x00000a63      488b45d8       mov rax, qword [local_28h]
|      |    0x00000a67      4889c7         mov rdi, rax
|      |    0x00000a6a      e85fffffff     call 0x9ce					; [2]
|      |    0x00000a6f      85c0           test eax, eax
|      |,=< 0x00000a71      750a           jne 0xa7d
|      ||   0x00000a73      b800000000     mov eax, 0
|     ,===< 0x00000a78      e9b1000000     jmp 0xb2e
|     ||`-> 0x00000a7d      48c745e80000.  mov qword [local_18h], 0
|     ||,=< 0x00000a85      eb3f           jmp 0xac6
|    .----> 0x00000a87      488b45e8       mov rax, qword [local_18h]
|    :|||   0x00000a8b      488d5001       lea rdx, qword [rax + 1]
|    :|||   0x00000a8f      488b45d8       mov rax, qword [local_28h]
|    :|||   0x00000a93      4801d0         add rax, rdx                ; '('
|    :|||   0x00000a96      0fb600         movzx eax, byte [rax]
|    :|||   0x00000a99      0fbed0         movsx edx, al
|    :|||   0x00000a9c      488b4dd8       mov rcx, qword [local_28h]
|    :|||   0x00000aa0      488b45e8       mov rax, qword [local_18h]
|    :|||   0x00000aa4      4801c8         add rax, rcx                ; '&'
|    :|||   0x00000aa7      0fb600         movzx eax, byte [rax]
|    :|||   0x00000aaa      0fbec0         movsx eax, al
|    :|||   0x00000aad      89d6           mov esi, edx
|    :|||   0x00000aaf      89c7           mov edi, eax
|    :|||   0x00000ab1      e8d4feffff     call 0x98a				; [4]
|    :|||   0x00000ab6      85c0           test eax, eax
|   ,=====< 0x00000ab8      7507           jne 0xac1
|   |:|||   0x00000aba      b800000000     mov eax, 0
|  ,======< 0x00000abf      eb6d           jmp 0xb2e
|  |`-----> 0x00000ac1      488345e802     add qword [local_18h], 2
|  | :|||      ; JMP XREF from 0x00000a85 (fcn.00000a36)
|  | :||`-> 0x00000ac6      488b45f8       mov rax, qword [local_8h]
|  | :||    0x00000aca      48d1e8         shr rax, 1
|  | :||    0x00000acd      483945e8       cmp qword [local_18h], rax  ; [3]
|  | `====< 0x00000ad1      72b4           jb 0xa87
|  |  ||    0x00000ad3      488b45f8       mov rax, qword [local_8h]
|  |  ||    0x00000ad7      48d1e8         shr rax, 1
|  |  ||    0x00000ada      488945f0       mov qword [local_10h], rax
|  |  ||,=< 0x00000ade      eb3f           jmp 0xb1f
|  | .----> 0x00000ae0      488b45f0       mov rax, qword [local_10h]
|  | :|||   0x00000ae4      488d5001       lea rdx, qword [rax + 1]
|  | :|||   0x00000ae8      488b45d8       mov rax, qword [local_28h]
|  | :|||   0x00000aec      4801d0         add rax, rdx                ; '('
|  | :|||   0x00000aef      0fb600         movzx eax, byte [rax]
|  | :|||   0x00000af2      0fbed0         movsx edx, al
|  | :|||   0x00000af5      488b4dd8       mov rcx, qword [local_28h]
|  | :|||   0x00000af9      488b45f0       mov rax, qword [local_10h]
|  | :|||   0x00000afd      4801c8         add rax, rcx                ; '&'
|  | :|||   0x00000b00      0fb600         movzx eax, byte [rax]
|  | :|||   0x00000b03      0fbec0         movsx eax, al
|  | :|||   0x00000b06      89d6           mov esi, edx
|  | :|||   0x00000b08      89c7           mov edi, eax
|  | :|||   0x00000b0a      e89dfeffff     call 0x9ac				; [5]
|  | :|||   0x00000b0f      85c0           test eax, eax
|  |,=====< 0x00000b11      7507           jne 0xb1a
|  ||:|||   0x00000b13      b800000000     mov eax, 0
| ,=======< 0x00000b18      eb14           jmp 0xb2e
| ||`-----> 0x00000b1a      488345f002     add qword [local_10h], 2
| || :|||      ; JMP XREF from 0x00000ade (fcn.00000a36)
| || :||`-> 0x00000b1f      488b45f0       mov rax, qword [local_10h]
| || :||    0x00000b23      483b45f8       cmp rax, qword [local_8h]
| || `====< 0x00000b27      72b7           jb 0xae0
| ||  ||    0x00000b29      b801000000     mov eax, 1
| ||  ||       ; JMP XREF from 0x00000b18 (fcn.00000a36)
| ||  ||       ; JMP XREF from 0x00000abf (fcn.00000a36)
| ||  ||       ; JMP XREF from 0x00000a78 (fcn.00000a36)
| ||  ||       ; JMP XREF from 0x00000a5e (fcn.00000a36)
| ``--``--> 0x00000b2e      c9             leave
\           0x00000b2f      c3             ret
```

The code first checks the length of the serial at `[1]`. If the length isn't
equal to 0x18 (24), the code exits. Next, at `[2]`, another function is called.
If that function returns 0, the code also exits. It turns out that this function 
simply calls `isalnum()` in a loop. If one of the characters in the string isn't
an alphanumeric character, the function returns 0, resulting in failure.


At `[3]` is a loop check that breaks the first loop when we have looped over the
first half of the serial. Shifting to the right by two is the same as dividing
by 2, e.g. `4 >> 1 = 2`.

The next loop works on the upper half of the serial. In both of the loops, a
function is called, checking two characters at a time. See `[4]` and `[5]`.

Let's take a look at these functions:


```bash
0x0000098a      55             push rbp
0x0000098b      4889e5         mov rbp, rsp
0x0000098e      89fa           mov edx, edi
0x00000990      89f0           mov eax, esi
0x00000992      8855fc         mov byte [rbp - 4], dl
0x00000995      8845f8         mov byte [rbp - 8], al
0x00000998      0fb645fc       movzx eax, byte [rbp - 4]
0x0000099c      3245f8         xor al, byte [rbp - 8]
0x0000099f      83f042         xor eax, 0x42
0x000009a2      3c45           cmp al, 0x45                ; 'E'
0x000009a4      0f9ec0         setle al
0x000009a7      0fb6c0         movzx eax, al
0x000009aa      5d             pop rbp
0x000009ab      c3             ret

0x000009ac      55             push rbp
0x000009ad      4889e5         mov rbp, rsp
0x000009b0      89fa           mov edx, edi
0x000009b2      89f0           mov eax, esi
0x000009b4      8855fc         mov byte [rbp - 4], dl
0x000009b7      8845f8         mov byte [rbp - 8], al
0x000009ba      0fb645fc       movzx eax, byte [rbp - 4]
0x000009be      3245f8         xor al, byte [rbp - 8]
0x000009c1      83f013         xor eax, 0x13
0x000009c4      3c1e           cmp al, 0x1e
0x000009c6      0f9fc0         setg al
0x000009c9      0fb6c0         movzx eax, al
0x000009cc      5d             pop rbp
0x000009cd      c3             ret
```

The first function xor's the arguments with each other, and then with the
constant 0x42. The second function uses the constant 0x13 instead.

The first function compares the result against 0x45, if the result is less than
or equal to this number, the function results success (0). The second function
results success if the result is greater than 0x1e.

In pseudo-code, the check function looks something like this:

```C
static int check_1(char a, char b)
{
	return ((a ^ b ^ 0x42) < 70);
}

static int check_2(char a, char b)
{
	return ((a ^ b ^ 0x13) > 30);
}

static int valid_serial(const char *buf)
{
	size_t len = strlen(buf);

	if (len != 0x18)
		return 0;

	if (!is_alphanumeric(buf))
		return 0;

	for (size_t i = 0; i < (len / 2); i += 2) {
		if (!check_1(buf[i], buf[i + 1]))
			return 0;
	}

	for (size_t i = (len / 2); i < len; i += 2) {
		if (!check_2(buf[i], buf[i + 1]))
			return 0;
	}

	return 1;
}
```
Note that upon connecting to the service we are actually asked to enter 250 serial keys as is suggested in the readme. This is because the task server is only using this binary to verify a serial key, which is why there is no flag printing function in this binary itself. The server part itself is written in python and looks like this:

```python
#!/usr/bin/env python3
from subprocess import run, PIPE
import sys

def read_flag():
    return open("/home/tghack/flag.txt").read()

def check_serial(s):
    proc = run(["/home/tghack/key_check.elf"], input=(s + "\n").encode("utf-8"), stdout=PIPE)
    return not proc.returncode
    
def main():
    serials = []
    for i in range(250):
        s = input("serial {}/{}: ".format(i + 1, 250))
        if not check_serial(s):
            print("Wrong! Try again")
            sys.exit()
        if s in serials:
            print("You already used that serial!")
            sys.exit()

        serials.append(s)
        if i != 249:
            print("Ok, next!")

    print("Thank you so much!")
    flag = read_flag()
    print("Here's the flag: {}".format(flag))

if __name__ == "__main__":
    main()
```
If you want to try this task yourself, we suggest that you build the a docker image from the included dockerfile.
A popular tool for solving key-gens, weak hash functions, etc is z3. This is a
great tool by Microsoft research. It is a SAT/SMT solver, which can be viewed as
a tool to solve a huge system of equations. See
[this](https://yurichev.com/writings/SAT_SMT_by_example.pdf) incredible book by
Dennis Yurichev for more details on Z3.

The first step is to convert the checker functions to Python/Z3.


```python
from z3 import *

s = Solver()

serial = [ BitVec("{}".format(i), 32) for i in range(24) ]
for i in range(24):
    # ascii
    s.add(serial[i] >= 48)
    s.add(serial[i] <= 122)
    s.add(serial[i] != ord(":"))
    s.add(serial[i] != ord(";"))
    s.add(serial[i] != ord("<"))
    s.add(serial[i] != ord("="))
    s.add(serial[i] != ord(">"))
    s.add(serial[i] != ord("?"))
    s.add(serial[i] != ord("@"))
    s.add(serial[i] != ord("\\"))
    s.add(serial[i] != ord("["))
    s.add(serial[i] != ord("]"))
    s.add(serial[i] != ord("^"))
    s.add(serial[i] != ord("_"))
    s.add(serial[i] != ord("`"))


for i in range(0, 12, 2):
    a = serial[i]
    b = serial[i + 1]
    s.add((a ^ b ^ 0x42) < 70)

for i in range(12, 24, 2):
    a = serial[i]
    b = serial[i + 1]
    s.add((a ^ b ^ 0x13) > 30)

# https://yurichev.com/writings/SAT_SMT_by_example.pdf
# page 475
results = []
while True:
    if len(results) >= 250:
        break
    if s.check() == sat:
        m = s.model()
        #print m[serial]
        #print m
        results.append(m)

        block = []
        for d in m:
            if d.arity() > 0:
                raise Z3Exception("uninterpreted functions are not supported")
            c = d()
            if is_array(c) or c.sort().kind() == Z3_UNINTERPRETED_SORT:
                raise Z3Exception("arrays and uninterpreted sorts are not supported")
            block.append(c != m[d])
        s.add(Or(block))
    else:
        print "results: {}".format(len(results))

def bv2int(bv):
    return int(str(bv))

serials = []
for res in results:
    serials.append("".join([chr(bv2int(res[serial[i]])) for i in range(24)]))
```

Running the script presents us with 250 valid serials :))

The only thing left is to add some code to send the serials to the server:
```python
r = remote("localhost", 2222)
for i in range(250):
	print(r.recvuntil(": "))
	r.sendline(serials[i])
	print(r.recvline())

r.interactive()
```


```bash
$ python2 solve.py
[...]
Here's the flag: TG19{you_sure_are_a_real_cracking_magician}
```
