# Using the pwn module to solve CTF-challenges

Now, dear witches and wizards, let's get started on solving some CTF challenges!
I hope you had fun going through the Python tutorial, and that you are ready to
push your skills even further.

Many CTF challenges require you to connect to some mystical service to show off
your magical abilities. Thankfully, there are libraries available to help us
communicate with services more easily. Good luck, and have fun!

<br>

### Introduction
In this part of the Python tutorial, we are going to discuss the Python library
called `pwntools`. Not all of you might be familiar with such a magical thing
as a library. Every programming language has tons of libraries that the
programmer has to use to work with the language. As we noticed earlier in the 
tutorial, we had to download packages to work with the language. When we did
that, we also downloaded lots of libraries. The libraries that come with the
language are called the standard libraries. However, not all standard libraries
have all the functionality needed, and other non-standard libraries make it
easier for us to create scripts or programs. The library that we will use in
this tutorial, called pwntools, is exactly that: a non-standard Python library
to make it easier for us to solve CTF challenges.

According to the official pwntools documentation, pwntools is a `CTF framework
and exploit development library`. It is a python2 library and it greatly
simplifies interacting with remote and local services. We will use this library
since it has functionality not available in the standard python libraries. The
knowledge you gain from this tutorial can be used directly in the pwn n00b
tasks. In this tutorial, we focus on learning the basics of pwntools. 
This includes connecting to a remote service, ---sending and receiving
data, and manually interacting with the service. pwntools has a lot of
functionality not covered by this short tutorial, so if you want to know more,
take a look at some of the resources at the end of the tutorial.

All the code snippets in the following sections should be saved in a text editor
of your choice. You can then run the script by using the `python2` command from
the terminal.

We will solve two different tasks using pwntools in this tutorial. Good luck!

<br>

### Installation
In order for us to use pwntools, we have to install it first. The following
example works on Debian-based distributions. These are Linux distributions based
on Debian, and includes Ubuntu, Lubuntu, Xubuntu, Debian, and others. To install
the library, open the terminal on your machine, and enter the following
commands:
```
$ sudo apt-get update
$ sudo apt-get install python2.7 python-pip python-dev git libssl-dev libffi-dev build-essential
$ sudo pip install --upgrade pip
$ sudo pip install --upgrade pwntools
```

If you have trouble installing pwntools on your machine, please don't hesitate
to ask for help on the TG:Hack Discord!

<br>

### Getting Started
Now that we have installed pwntools to our machines, we may start using it while
building solution scripts. The first thing we have to do is to import all
functions from the library. You can do that by opening a file called
`[something_cool].py` in a text editor. Then, at the top of the file, add the
code from the snippet below. This snippet will import all the functionality that
pwntools provides.
```python
from pwn import *
```

Note: Don't name your file `pwn.py`, as Python will search the current directory
for modules named `pwn` first. And since we have named our script pwn.py, it
will try to import from itself. For more information see
[here](https://docs.python.org/2/tutorial/modules.html#the-module-search-path).

One of the strengths of pwntools is that we can connect to any service, and then
interact with it programmatically. We can read and write data with ease using
the provided functionality of the library.

We have set up a tiny service at `fortune.tghack.no` that will send you random
messages every time you connect to it. We can test the service by using a common
CTF-tool named `netcat`, or `nc` for short. This is a nice tool that allows you
to connect to any service and interact with it manually. If you connect to the
fortune service with netcat, you will be able to see all the data that is sent
from the service in your terminal. In CTFs, netcat is mostly used to connect to
services and send some data back and forth. netcat can, however, be used as a
network debugging tool, for example, since it can create many different types of
connections (TCP, UDP, DCCP, etc). To read more about netcat, check out the man
pages (`man netcat`), or [this](https://en.wikipedia.org/wiki/Netcat) Wikipedia
article.

```bash
$ nc fortune.tghack.no 3333
Q:	What's hard going in and soft and sticky coming out?
A:	Chewing gum.
$ nc fortune.tghack.no 3333
You are taking yourself far too seriously.
```

Okay, great. Now let's try to replicate this functionality with pwntools!
Remember to put the following code in a script. If you name the script
`solve.py`, you can use it by running `python2 solve.py` in your terminal.

We can start by creating a connection to `fortune.tghack.no`:
```python
from pwn import *
r = remote("fortune.tghack.no", 3333)
```

We can then receive and print one line from the server by adding the following:
```python
line = r.recvline()
print line
```

Here's the full script:
```python
from pwn import *

r = remote("fortune.tghack.no", 3333)
line = r.recvline()
print line

# close the connection, not really needed
r.close()
```

We have set up a service to help you practice some pwntools skills at
`echo.tghack.no:5555`. Your task is to echo back everything that is printed by
the server. If you do this 50 times in a row, you will get the flag!
To send data, you can use `send()` or `sendline()` depending on if you want a
newline at the end or not.

For example, if you want to first send the text `hello` followed by `, world!`
and a newline at the end, you could do it like this:
```python
r.send("hello")
r.sendline(", world")
```
And the server would receive `hello, world!`.

<br>

### Echo Chamber
You should be ready to tackle the Echo Chamber challenge now. Good luck, and
have fun! You can find the challenge under the n00b category at
[tghack.no](https://tghack.no).

<br>

### Other Functions
Several other functions exist to receive data. One of the more useful functions
for this is `recvuntil()`, which lets you receive data up until some known
string. If a server sends you the message "Hello, world", and you only want the
letters after the first space, you can use `recvuntil()` like this:
```python
r.recvuntil(" ")
world = r.recvline().strip()
print world # prints "world"
```

pwntools has a nice feature called `interactive mode`. This mode allows you to
interact with the server as if you were using a terminal. Interactive mode is
very useful when you have to type something manually, which is a common scenario
when solving pwn tasks, as you often end up with a shell. After getting a shell,
you might have to explore the file system to find the file containing the flag.
To put the connection in interactive mode, simply run `r.interactive()`. Press
ctrl+C to get out of interactive mode again.

<br>

### The Calculator
Equipped with a few functions from pwntools and the corresponding documentation,
you should be ready to test your newfound skills with mythical languages against
our calculator challenge. You can find the challenge under the n00b category at
[tghack.no](https://tghack.no).

<br>

### Resources
[pwntools docs](https://docs.pwntools.com/en/stable/)
