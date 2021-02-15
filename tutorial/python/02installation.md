# Python installation
Hi! Welcome to the second lesson of the Pythontongue class. Today, we will do some
preparations. The Pythontongue isn't something that every wizard and witch knows 
by default. We have to install it before starting with the main lessons. This step of the 
tutorial will show you how to install Python, and how you can check that it was installed properly. 
If you already have Python 2.7 installed, you may move on to the next
step of the Python tutorial. 

_Note that we will use Python 2.7 in this class, because some of the tools
we are going to use are only supported in this version of Python._

<br>

## Install Python
There is mainly one thing to think about when installing Python, and that is 
which operating system (OS) you use. Windows and macOS are examples of
operating systems. However, hackers and CTFers usually use an OS which is 
based on Linux. Examples of common operating systems that are based on 
Linux are Ubuntu, Kali Linux, and Arch Linux. We call these Linux distributions. 
Kali Linux is often recommended for use in ethical hacking courses because it
contains lots of hacker tools by default. Ubuntu is often recommended if you 
are new to Linux. So, based on what OS you use, choose a section below for 
instructions on how to install Python.

To install Python on a fresh Linux distribution (On Ubuntu, Debian or similar
distributions),
you can run these commands:

```
sudo apt update
sudo apt install python python-pip
```

---

__If you use Fedora or CentOS:__

```
sudo dnf update
sudo dnf install python python-pip
```

---

__If you use windows (Not recommended for CTFs, but since you insist...):__

Visit https://python.org and download your desired python
version. Remember to install the python launcher when asked during the installation.
In windows the python executable is called python.exe both for version 2 and 3.
However, the different versions have different file paths.
The Python launcher can be used to more easily choose the right python version,
because it finds all the different versions for you automatically.
This way you can use `py -2` and `py -3` instead of the Linux equivalent
`python2` and `python3`.

During this class we will use Linux. You are free to choose which OS
you want to use, but we will only cover Linux from now on.

<br>

## Check your Python installation

When you have installed Python on your machine, check
which version of Python you are running:

`python --version`

You can specify which version of Python you want to run by adding
version numbers at the end of `python`. If you have multiple Python2 or
Python3 versions, `python3` runs the latest Python3 version installed on
your machine and `python` or `python2` runs the latest Python2 version.

Example:

```bash
> python --version
Python 2.7.14
```

```bash
> python2 --version
Python 2.7.14
```

_Python 2_ and _Python 3_ have quite a few differences in their implementation.
However, you will most likely not notice these differences right away unless you
read through the documentation. We will not talk about all of the differences in
this class, but you will definitely encounter that the `print` function is
implemented differently. Often you can run _Python 3_ code in _Python 2_ and
vice versa, since there are many things they have in common, but not always. In
_Python 3_, `print` is a function, and you need to wrap what you want to print
in parentheses (`print('Hello')`). In _Python 2_, `print` is a statement, so you
can just write what you want to print after a space (`print 'Hello'`).

<br>

## Check your Pip installation

You will learn about Pip later. For now, just check that it is correctly
installed.

__Upgrade pip__

`pip install --upgrade pip`

The command to check your Pip version is pretty similar to the Python one above.

```bash
> pip --version
pip 18.1
```

Good! Now we have what it takes to use the great powers of the Pythontongue.
The next lesson of the tutorial introduces the Pythontongue language, and you
are getting started with writing magical spells on your script rolls! 
