# Bytecodes writeup
**Points: 50**

**Author: PewZ**

**Difficulty: easy**

**Category: reversing**

---

Let's take a look at the `pyc` file we are given in the task:

```bash
$ file main.pyc
main.pyc: python 3.6 byte-compiled
```

If you are familiar with Python, you have probably seen `.pyc` files before.
If not, this is an optimized version of a python script, stored as something
called bytecode. Instead of representing the code as normal text, bytecode
stores the code as bytes, which have special meaning for the Python interpreter.

If you want to know more about Python bytecode, you can read
[this](https://opensource.com/article/18/4/introduction-python-bytecode) nice
article.

The act of turning bytecode into readable code is known as
[decompilation](https://en.wikipedia.org/wiki/Decompiler). If we Google a bit
for "how to decompile pyc", for example, we quickly stumble over
[uncompyle6](https://pypi.org/project/uncompyle6/). Which, according to the
description on pypi, is "a native Python cross-version decompiler and fragment
decompiler". 

Let's install the tool and run it:
```bash
$ sudo pip3 install uncompyle6
[...]
$ uncompyle6 main.pyc
# uncompyle6 version 3.2.6
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.7 (default, Oct 22 2018, 11:32:17) 
# [GCC 8.2.0]
# Embedded file name: main.py
# Compiled at: 2019-04-13 14:56:41
# Size of source mod 2**32: 514 bytes
import binascii, sys

def print_flag():
    enc = '1605737b39323b362a2d2c1d203b3627212d26271d2b2c1d362a271d2a2d3731273f'
    enc = binascii.unhexlify(enc)
    key = 66
    dec = ''
    for i in enc:
        dec += chr(i ^ key)

    print(dec)


def main(code):
    if code == 1337:
        print_flag()
    else:
        print('wrong!')


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('error! missing magic code!')
        sys.exit()
    main(int(sys.argv[1]))
# okay decompiling main.pyc
```

Nice, we have successfully recovered the Python source code! We can see that the
program asks for a magic code, and then checks to see if this value is 1337. If
the value matches, the `print_flag()` function is called.

Let's try passing `1337` as the only argument:

```bash
$ python3 main.pyc 1337
TG19{python_bytecode_in_the_house}
```
