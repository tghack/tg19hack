# Using Crypto Modules in Python

Cryptography can be a difficult topic, and not all programming languages have
good support for crypto libraries to make scripting of cryptography related
tasks easier. Fortunately, Python has some nice libraries that we can use to
solve CTF tasks [pertaining](http://lmgtfy.com/?q=pertain) to cryptography.
In this tutorial, we will be using
[pycrypto](https://github.com/dlitz/pycrypto). This library has support for all
the functionality we need for basic crypto tasks.

<br>

### Installation
To install pycrypto, we can use `pip` in the terminal like we did in the
previous part of the Python tutorial series:
```bash
$ sudo pip install pycrypto
```

If you don't have `pip` installed, install it using the following command in the
terminal:
```bash
$ sudo apt install -y python-pip
```
<br>


### Numbers
We often have to convert between bytes and numbers when working with
cryptography. When data is stored in a file, or sent over the network, it will
be stored or sent as a sequence of bytes. In Python, we need to convert these
sequences of bytes to numbers, so that we can perform calculations on them.

Conversion between numbers and bytes are done using the following
functions:
* `bytes_to_long`: Converts bytes to numbers.
* `long_to_bytes`: Converts numbers to bytes.


When testing short snippets of Python code, it's very handy to use an
interactive Python shell in the terminal. One such program is `ipython`, and you
can install it using: `sudo apt install -y ipython`. `ipython` is commonly used
when prototyping or when testing how a function or module works. The following
snippet shows an example of how an ipython session looks. In the shell, we
convert 1337 to bytes, and back again to a number.

```bash
$ ipython
Python 2.7.15rc1 (default, Nov 12 2018, 14:31:15)
Type "copyright", "credits" or "license" for more information.

IPython 5.5.0 -- An enhanced Interactive Python.
?         -> Introduction and overview of IPython's features.
%quickref -> Quick reference.
help      -> Python's own help system.
object?   -> Details about 'object', use 'object??' for extra details.
In [1]: from Crypto.Util.number import bytes_to_long, long_to_bytes

In [2]: long_to_bytes(1337)
Out[2]: '\x059'

In [3]: b = long_to_bytes(1337)

In [4]: bytes_to_long(b)
Out[4]: 1337L
```

At `[1]`, we import the required functions from pycrypto. Then we convert 1337
to bytes at `[2]`. The conversion from bytes to a number can be seen a `[3]` and
`[4]`.

These functions may seem a bit pointless now, but if you Google something like
`CTF writeup long_to_bytes` you will find a lot of writeups using these
functions, and other functionality from pycrypto :) In other words, this is good
practice for solving CTF tasks in the future. 

<br>

### Numbers or Bytes?
To practice, we have set up a task called `Numbers or Bytes?` in the n00b
category.  
The task asks you to convert between numbers and byte strings. You will have to
do this 10000 times to get the flag. If you haven't checked out the previous
chapter in this tutorial, you should do that first, since using pwntools will
help you a lot when solving this challenge.

<br>

### Hash Functions
A hash function is a function that takes an arbitrary amount of data as input,
and outputs a fixed amount of data. The function can take a whole file of many
gigabytes, or a small program of a couple of megabytes. Even a single character.
The output, however, will always be the same size. In addition, the output will
always be the same. Just a slight change in output will cause the output to be
dramatically different. See the following example, where we have the MD5 hashes
of `foobar123` and `foobar124`:

```
foobar123:ae2d699aca20886f6bed96a0425c6168
foobar124:0ae368c4e2f530c63438c4f719e7704b
```

In cryptography, hash functions that are very difficult to reverse are used.
This means that, in practice, it should be impossible to go from a hash and back
to the original data that was used.

The return value of a hash function is called a hash value, message digest,
digest, or checksum.

Uses of hash functions include verifying the integrity of files, password
verification, and signature generation. In some of the tasks that we have in
this CTF, you will be provided with a hash in addition to a file. This hash
enables you to verify that the file has been downloaded correctly, and isn't
tampered with in any way.


Here's an example of how we can hash the message "TG:Hack ftw" using SHA256 in
Python:
```python
from Crypto.Hash import SHA256
hash = SHA256.new()
hash.update("TG:Hack ftw")
print hash.hexdigest()
```
Running it prints:
```bash
$ python2 hash.py
7b0cdbc93ad4acb5b7b0cdf8cf66de7bd5f743cae07305ee1b52334795f820cd
```

Check out the PyCrypto
[documentation](https://www.dlitz.net/software/pycrypto/api/current/) for a list
of supported hash functions.

<br>

### Let's Hash it Out
We created a task for you that lets you try out different hash functions in
Python. The task is called `Let's Hash it Out`, and you can find it in the n00b 
category at [tghack.no](https://tghack.no).
The goal is to hash different strings using several hash functions. Like many
of the other n00b tasks, you will have to do this 10000 times to get the flag.
Good luck!

<br>

### Resources
* [pycrypto](https://github.com/dlitz/pycrypto)
