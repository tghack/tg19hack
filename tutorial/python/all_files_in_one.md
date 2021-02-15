# Scripting in Pythontongue

Welcome to a new year at the School of Wizardry! You wizards and witches
will face many challenges this year. In order to be prepared for these challenges,
we created this class about mythical languages and codes.
Mythical languages can help you on your quest to solve challenges, but first you must be
able to use them.
This year you will learn about a particular language I am sure you have heard about:
_Pythontongue_, or _Python_ for short!


I am professor _Zup_. Professor _PewZ_ and I will be your professors in this class.
The language you will learn has many magical features. If you get good at it,
you can do almost anything you want. Using the _Python_ language you write spells and
codes on script rolls. It is up to you to tell the scripts what to do.

## Agenda for the class

This class will consist of several parts. First you learn how to set up your learning
environment.
After that, there are several parts on how the _Python_ language is structured.
At the end you will be able to solve CTF-challenges by using everything you have learned about
this magical language.

If you know Python, but the Python pwn modules or crypto modules are 
new for you, jump straight to lesson 5 and 6! 


**Class plan:**

| Class topic | Description | Teacher |
|:-----------:|:-----------:|:-------:|
| Installation of __Python__ and __Pip__ | You will learn about setting up a learning environment that will help us interpret the _Python_ language | Professor Zup
| Introduction to __Python__ and __variables__ | Basic intro on how _Python_ works, variable types and operations you can do on different variable types. | Professor Zup
| __Boolean operators__, __conditionals__ and __loops__ | Learn about functionality that will help you control the flow in your code. | Professor Zup
| __Functions__, __classes__ and __modules__ | How do you make your code cleaner and more intuitive? Learn about _functions_ and _classes_ | Professor Zup
| __Regular expressions__ | Regular expressions will help you find what you are looking for in a text. Learn about how it works! | Professor Zup
| __File handling__ and __Exceptions__ | Reading and writing to files is really helpful some times. Learn about _file handling_, _context managers_, _exception handling_ | Professor Zup
| Using the __pwn__ module | Using the pwn module to solve CTF-challenges | Professor PewZ
| Using __crypto__ modules | Using crypto modules to solve CTF-challenges | Professor PewZ

<br>

### Exams giving magical XP points
There are four exams related to this class. In the two last parts of the Python 
tutorial, you will be presented with the exams that you might be ready to take. 
All of the exams may be found in the n00b category in the tasks page. Here is a 
list of the exams:

| Exam name | Points |
|:---------:|:------:|
| Echo Chamber | 5 |
| Math Bonanza | 10 |
| Numbers or Bytes? | 15 |
| Let's Hash it Out | 20 |

<br>

## Guidelines for code snippets

During each topic, we show you code examples. A single example usually consists
of two code snippets. First the source code, followed by the
output printed when the code is executed. Take a look at the following example:

Here is a snippet of a _Python_ script printing the text "Hello, magical world!"

```python
print "Hello, magical world!"
```

And here is the output of the snippet:

```sh
Hello, magical world!
```

Keep this in mind throughout the class, I'm sure you'll do great!

<br>

# Python installation
Hi! Welcome to the second lesson of the Pythontongue class. Today, we will do some
preparations. The Pythontongue isn't something that every wizard and witch knows 
by default. We have to install it before starting with the main lessons. This step of the 
tutorial will show you how to install Python, and how you can check that it was installed properly. 
If you already have Python 2.7 installed, you may move on to the next
step of the Python tutorial. 

_Note that we will use Python 2.7 in this class, because some of the tools we are going to use are only supported in this version of Python._

## Not using Linux? Start now!
For the last two lessons in this Pythontongue tutorial, and the third tutorial, 
the Pwntions tutorial, you must have a Linux environment, as the tool you will
be using, pwntools, requires it. Linux is an operating system (OS). Windows and 
macOS are examples of
operating systems. However, hackers and CTFers usually use an OS which is 
based on Linux. Examples of common operating systems that are based on 
Linux are Ubuntu, Kali Linux, and Arch Linux. We call these Linux distributions. 
Kali Linux is often recommended for use in ethical hacking courses because it
contains lots of hacker tools by default. Ubuntu is often recommended if you 
are new to Linux. 

If you have a Windows or Mac, we recommend that you use a virtual machine (VM).
You may get a VM by downloading
[VirtualBox](https://www.virtualbox.org/wiki/Downloads).
VirtualBox is a software on your machine that emulates another machine. On that machine,
you should install Ubuntu or Kali. 

_Choose whether you want to use Kali Linux or Ubuntu:_

- __Kali__: You can download a 64-bit Kali Linux .ova file from 
    [here](https://images.offensive-security.com/virtual-images/kali-linux-2019.1-vbox-amd64.ova).
    The Kali OS is preinstalled in this virtual machine, so just open the .ova file in Virtualbox, 
    and it should work right away (log in with `root`/`toor`)!
- __Ubuntu__: Note that this takes a bit more time than Kali, since we need to install the OS on the VM.
    First, download an image of Ubuntu 18.04 from [this site](https://www.ubuntu.com/download/desktop). 
    To get detailed information on how to install Ubuntu in VirtualBox, please follow 
    [this guide](https://helpdeskgeek.com/linux-tips/how-to-install-ubuntu-in-virtualbox/).
    It illustrates how to setup a VM and install the Ubuntu image on the VM.
    Please note that your virtual machine will run slowly if you use 32-bit, so
    you should use 64-bit. Also, it says 1024 MB of memory (RAM), but if your machine
    allows, we recommend 2048 MB. If you have space, maybe choose 30 GB of space 
    instead of the 10 GB in the guide. Also, when it says `Erase disk and install Ubuntu`,
    it means it will erase the disk of the virtual machine, not your computer. 

## Install Python
There is mainly one thing to think about when installing Python, and that is 
which operating system (OS) you use.  So, based on what OS you use, choose 
a section below for instructions on how to install Python.

To install Python on a fresh Linux distribution (On Ubuntu, Debian or similar
distributions),
you can run these commands:

```sh
sudo apt update
sudo apt install python python-pip
```

__If you use Fedora or CentOS:__

```sh
sudo dnf update
sudo dnf install python python-pip
```


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

## Check your Python installation

When you have installed Python on your machine, check
which version of Python you are running:

```bash
python --version
```

You can specify which version of Python you want to run by adding
version numbers at the end of `python`. If you have multiple Python2 or
Python3 versions, `python3` runs the latest Python3 version installed on
your machine and `python`(usually) or `python2` runs the latest Python2 version.

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

## Check your Pip installation

You will learn about Pip later. For now, just check that it is correctly
installed.

__Upgrade pip__

```bash
> pip install --upgrade pip
```

The command to check your Pip version is pretty similar to the Python one above.

```bash
> pip --version
pip 18.1
```

Good! Now we have what it takes to use the great powers of the Pythontongue.
The next lesson of the tutorial introduces the Pythontongue language, and you
are getting started with writing magical spells on your script rolls! 

# Python introduction and variables
In this lesson of the Pythontongue class, we demonstrate how to write
spells properly on script rolls. To begin with, we discuss the different
types of script rolls to write on. Then we move on to how we write something
called _variables_ in the Pythontongue, and what types of variables exists in the
language. We explain what a variable is later on. This is basic knowledge
to make sure you are ready to write powerful spells on your script rolls. 

___A quote from [python.org](https://docs.python.org/2/tutorial/)'s own tutorial___

_"Python is an easy to learn, powerful programming language. It has efficient high-level data structures and a simple but effective approach to object-oriented programming. Python’s elegant syntax and dynamic typing, together with its interpreted nature, make it an ideal language for scripting and rapid application development in many areas on most platforms"_ 

## Several ways to write Pythontongue

### Python Shell

The simplest way to use Python is the built-in Python shell.
This shell is mostly used to run small amounts of code, and you don't have to create any files to execute this code.

To start the shell type the command `python` or `python2` in your terminal. When you are inside the Python shell, you can type code
that gets executed as soon as you press enter. You have to write the code one line at a time.

To exit the shell you can call the function `quit()`

```bash
user@tg19:~$ python2
>>> print 'Hello world'
Hello world
>>>
```

<br>

### Straight from the terminal

There is also a way to execute Python code straight from the terminal without entering a Python shell.
Just add a `-c` flag like the example below

```bash
user@tg19:~$ python2 –c "print 'Hello world'"
Hello world
user@tg19:~$
```

<br>

### As a regular Python script

Most of the time when you want to create a Python program, you will be creating files containing Python code.
Python scripts usually have the `.py` file extension, but this is not necessary to run them.

Let's create our first Python script:
1. Create a file named `hello.py`
2. Write the following code into the file and save it:

```python
 #!/usr/bin/env python2
 # This is a comment! You can comment out text using the '#' symbol. A comment will not get executed.
 print 'Hello world'
```

3. Run the code

```bash
user@tg19:~$ python hello.py
Hello world
user@tg19:~$
```

The first line in `hello.py` is called a _shebang_. In Linux or Unix based systems, the _shebang_ is a way
to make text files executable. It defines which interpreter to run the file with.
In `hello.py` we specified that it should be run using the _python_ interpreter.

If a _shebang_ is present and the file is executable, we can run it using
`./hello.py` instead of `python hello.py`. If you only want to run it using the latter, it is not
necessary to have a _shebang_. You can make the file an executable by running 
`chmod u+x hello.py` in the terminal.  [Read more about _shebangs_ here](https://en.wikipedia.org/wiki/Shebang_%28Unix%29)

---

<br>

## Variables

Variables are used to store values you want to access at a later time. You can think of variables as stickers put on objects.
Every sticker has a unique name written on it (_a variable name_), and it can only be on one object at a time.
You can put more than one sticker on the same object, if you want to. However if you put an already
attached sticker on another object, the sticker will move from the old to the new object.

<details>
  <summary>What is initialization and declaration?</summary><p>
  Initialization and declaration are quite similar and easy to get confused by. 
  They are terms used when writing new variables in your code. The 
  terminology is the same for most programming languages. So, when you 
  initialize a variable, you give the variable a value. However, if you 
  declare a variable, you just give it a name without variable. Take a look
  at these examples:

  * Initializing a variable: `my_variable = 10`
  * Declaring a variable: `my_variable`

  Note that the latter is not allowed in Python, as mentioned in the first 
  bullet point in the next section. 
</p></details><br>

### Basic info
- Variables in Python must be initialized explicitly. This means you must give a value
to the variable when you declare it. In other languages like C or C++, it is
possible to declare a variable without giving it a value.

- Another unique thing about Python is that it's not necessary to define a type for the variables
you declare. The interpreter will automatically find the types for each variable based on which
value they have been given.
For example: `my_int = 3` will be an _integer_ while `my_str = "Example"` will be a _string_ type.

- `None` is Python's version of a `null` value. `None` is just a value that commonly is used
to signify _"empty"_ or _"no value here"_.

- Scoping is an essential part of variables and functions. A variable is only accessible inside of a specific scope.
__Global__ variables are declared outside any function, and they can be accessed (used) in any function in the
program. __Local__ variables are declared inside a function, and can be used only inside that function.
It is possible to have __local__ variables with the same name in different functions.
[Read more about local and global variables](https://funprogramming.org/50-What-are-global-and-local-variables.html)


<br>

### Variable Types
In this section, we discuss variable types and functions that might be helpful and nice 
to know about. We start by discussing strings, integers and floating point numbers, then 
we move on to lists and tuples, and end with a section about dictionaries. 

#### Text strings (str)
A string is usually a bit of text you want to display to someone, or
"export" out of the script you are writing. Python knows you want something
to be a string when you put either `"` (double-quotes) or `'` (single-quotes)
around the text:

```python
my_string = "Wizards"
my_string2 = 'Witches'
```

<br>

##### String operations
- Concatenation and multiplication
- Splitting
- Modification
- Testing
- Converting/Casting
- Formatting

<br>

__Concatenation and multiplication__

The process of joining strings together to form a single string is called concatenation.
To do this we can use the `+` operator.

```python
output = my_string + " and " + my_string2
print output
```

Output:

```bash
Wizards and Witches
```

It is also possible to use multiplication (`*`) to repeat a string.

```python
print "Lumos" * 4
```

Output:

```sh
LumosLumosLumosLumos
```

<br>

__Splitting__

The opposite of concatenation is splitting a single string into multiple strings. This can be done by
using a built-in method for the string object type. To call a method append `.<method name>()` to the object.
The two parentheses mean that we want to call the method. There is a method called _split_ we can use to split a string.

```python
print output.split()
```

Output:

```sh
['Wizards', 'and', 'Witches']
```

<br>

__Modification__

There are many methods used to modify string content. The methods return the modified value, but
does not change the original variable. Methods like _lower_ and _upper_ return the string in lower or uppercase
respectively. _Replace_ returns a string where a certain value has been replaced by something else.

```python
print output.upper()
print output
print output.replace('and', 'or')
```

Output:

```bash
WIZARDS AND WITCHES
Wizards and Witches
Wizards or Witches
```

[Check out this link](https://www.programiz.com/python-programming/methods/string) for a list of more string methods.

__Testing__

Using methods to test whether the string content is as expected.

Tests if the string only contains characters from the alphabet. Returns True or False

```python
print output.isalpha()
```

Output:

```sh
True
```

__Converting/Casting__

The method of converting other types into string types.

```python
print str(42) + ' ' + output
```

Output:

```sh
42 Wizards and Witches
```

<br>

__Formatting__

Formatting is a way of inserting variables and values into a string without
using concatenation.
There are many ways of formatting strings in Python.

```python
print "%s has learned %d spells this year!" % ('Thomas', 14)

print "{0} has learned {1} spells this year!".format('Hailey', 8)

print "I know {num_spells} different spells...".format(num_spells=7)
```

Output:

```sh
Thomas has learned 14 spells this year!
Hailey has learned 8 spells this year!
I know 7 different spells...
```

F-strings were introduced in Python 3.6. This is an even easier way to insert
variables or do operations inside of strings:

```python
days_left = 25
answer = f"There are {days_left * 5} days left of this semester."
print(answer)
```

Output:

```bash
There are 125 days left of this semester.
```

---

<br>

#### Integers (int)
Alright, so we just went through a lot of nice functions related to strings. Now, it is time 
to learn about numbers! Every programming language has some kind of way
of doing numbers and math, and this section describes how to handle integers. 
Integers are positive or negative whole numbers with no decimal point. 

##### Integer operations
- Printing variable type
- Math operations
- Type conversion

__Printing variable type__

Let's first take a look at integers and create some variables.

```python
wands = 6
owls = 17
frogs = 2
print type(wands)
```

By looking at the output, we can see that the variables are of the type _int_:

```bash
<type 'int'>
```

__Math operations__

As we know the variables are of the type _int_, we can do math operations using these variables.
Take a look at [this website](https://www.tutorialspoint.com/python/python_basic_operators.htm) for a
complete list of all basic operators in Python.

```python
wands = wands + 4
wands -= 1

print wands
print wands * owls + frogs
print 5**2
```

The following output shows the results of adding and multiplying the variables:

```bash
9
155
25
```

Now, lets trying dividing!

```python
print wands // frogs
```

The operator used above is integer division. Note that `9 // 2` returns an
integer and not a decimal number (float):

```sh
4
```

__Conversion__

Remember when we converted an integer to a string in the "Text string" chapter? We can also go the other way around:

```python
print 1 + 2 + 3 + int('4') + int('5')

print 1 + 2 + 3 + '4' + '5'
```

As you can see in the example below, we get a _TypeError_ if we don't convert
our strings to integers before the addition.

```bash
15

Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: unsupported operand type(s) for +: 'int' and 'str'
```

#### Floating point numbers (float)
Floats represent real numbers and are written with a decimal point dividing the integer and fractional parts.
Floats may also be in scientific notation, with E or e indicating the power of 10.

```python
print 3.2e2 == 3.2 * 10**2 == 320

print 5.5 + 19.5
print 9.0 / 2
```

Output:

```sh
True

25.0
4.5
```

We can also convert strings or integers to float values:

```python
print float(owls)
print float('56.55')
```

Output:

```bash
17.0
56.55
```

#### Lists and Tuples
Lists and tuples are ways to store multiple values in a sequence. Lists can be written as a sequence
of comma-separated values between square brackets. The items in a list does not have to be of the same type.
Tuples are sequences just like lists. The difference between lists and tuples is that lists are mutable
while tuples are immutable. In other words, tuples cannot be changed after initialized unlike lists.
Tuples also use parentheses around the items instead of square brackets.

##### List operations
- slice
- join
- sort
- pop
- remove
- insert
- append

Slicing makes it possible to get a specific range of items from lists, tuples
or custom data structures:

```python
magic = ['cloak', 'wand', 'spellbook']

print magic
print magic[1]
print magic[0:2]
```

Output:

```sh
['cloak', 'wand', 'spellbook']

wand

['cloak', 'wand']
```

The join operation returns a string from a list. Each item joined gets separated by a chosen separator:

```python
print 'My magic objects are ' + ', '.join(magic) + '.'
```

Output:

```bash
My magic objects are cloak, wand, spellbook.
```

Here is a tuple. Notice that it's not possible to change an item or add an item
to the tuple using the append method. This is because it is immutable.

```python
magical_numbers = (7, 9, 15, 42, '66')
magical_numbers.append(30)
```

```python
magical_numbers[2] = 12
```

Output:

```bash
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
AttributeError: 'tuple' object has no attribute 'append'
```

```bash
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: 'tuple' object does not support item assignment
```

More info about [lists](https://www.tutorialspoint.com/python/python_lists.htm) and
[tuples](https://www.tutorialspoint.com/python/python_tuples.htm)

<br>

#### Dictionaries (dict)
Dictionaries are just what they sound like; a collection of key/value pairs. Look up a key in the dictionary
to access its value. Each key is separated from its value by a colon (`:`), the items are separated by commas,
and the whole thing is enclosed in curly braces. Keys are unique within a dictionary while values may not be.
An empty dictionary without any items is written with just two curly braces, like this: `{}`

```python
wand = {'wood': 'Holly', 'core': 'Phoenix feather', 'price': 199}
wand['in_stock'] = 2

print wand
print wand['core']
print 'length' in wand
```

Output:

```sh
{'core': 'Phoenix feather', 'price': 199, 'wood': 'Holly', 'in_stock': 2}
Phoenix feather
False
```

In the code above, we initialize a dictionary and add a new key with the value `2`. We print out the value of
a specific key, _core_. At last we check if the key _length_ is in the dictionary. It is not.

Let us check out the _items_ method.

```python
print wand.items()
```

Output:

```sh
[('core', 'Phoenix feather'), ('price', 199), ('wood', 'Holly'), ('in_stock', 2)]
```

We get a list of tuples! The tuples contains the key and value of each
corresponding item in the dictionary.

Find more info about dictionaries [here](https://www.tutorialspoint.com/python/python_dictionary.htm).

<br>

## Summary and ending
Alright, brave students! You have been through a lot of new Pythontongue
functionality. We have learned some basics about the variable types _string_, 
_integer_, _list_ and _tuple_, and _dictionary_. Lots of information to grasp at once, 
but it will definitely pay off in hacking and programming challenges!

Having finished this lesson, and knowing that you can go back to look at the 
material any time, you are ready to do some more complex magic! See you in 
the next class!

<br>

# Boolean operators, if-statements and loops

![Pathways: V2hpdGUgYmVhci9KLkYuIERhdmllcw==](https://storage.googleapis.com/tghack-public/paths.jpg)

In this lesson you learn about the functionality that can be used to control the flow
of our code, such as boolean operators, if-statements and loops. Using this knowledge, 
you will be able to create more complex scripts than using only variables,
print functions and math. Let's begin the lesson, I hope you brought your tinfoil hats
for this one!

## Boolean operators

A boolean expression (or logical expression) evaluates to one of two states; _true_ or _false_.
Python provides the boolean type that can be either set to `False` or `True`.
Many functions and operations return boolean objects.

Every object has a boolean value. The following elements are false:

- `None`
- `False`
- `0` (Zero is false for all number types: integers, floats, complex numbers, etc.)
- Empty collections: `''`, `()`, `[]`, `{}`
- Objects from classes that have the special method `__nonzero__`
- Objects from classes that implements `__len__` to return `False` or `0`

If an object is not in any of the categories above, it's usually `True`.

There is also a way to inverse a boolean type:

```python
print not True
print not False
```

As the output of the print statements illustrate below, _True_ becomes _False_, and _False_ becomes  _True_ when you put _not_ in front of it.

```sh
False
True
```

The `not` keyword is very useful and is used a lot with comparison operators and if-statements.
Let's test different types and values by printing a string containing a value, followed 
by an equal sign ('=') and the _int_ or _bool_ representation of the same value:

```python
print "True  = ", int(True)
print "False = ", int(False)
print "1     = ", bool(1)
print "0     = ", bool(0)
print "-0.87 = ", bool(-0.87)
print "'g'   = ", bool('g')
print "''    = ", bool('')
```

The output below demonstrates what was mentioned earlier - that each object has a boolean value.
For instance, we see that an empty string is False, while a string containing a _g_ is True.
Similarly, the number 0 is False, while the number 1 is True.

```sh
True  =  1
False =  0
1     =  True
0     =  False
-0.87 =  True
'g'   =  True
''    =  False
```

### Comparison operators
The comparison operators compare the values of two objects and return either `True` or `False`.
The type of comparison is based on one of these operators:

- \< (less than)
- \<= (less than or equal to)
- \> (greater than)
- \>= (greater than or equal to)
- == (equal to)
- != (not equal to)

```python
print 10 == 10
print 3 < 9 <= 10
print 6 > 10
print "Lesson 5" == "Lesson 5"
```

```sh
True
True
False
True
```

Okay, so what happened here? In the first line we compare two numbers to check if
they are equal; `10` and `10`. They are equal so that means the result must be true.
The next comparison is a bit more complicated. Here we check that `9` is greater than `3`,
but at the same time less than or equal to `10`. This also seems to be true.
However in the next comparison we see that `6` is not greater than `10`, so the result is false.
Comparisons can also be used on strings or any other type of object.

[More on boolean and comparison operators](https://thomas-cokelaer.info/tutorials/python/boolean.html)

### AND and OR
To combine multiple comparisons you can use the _and_ and _or_ keywords.

- `and` is true if both values on each side of `and` are true.
- `or` is true if one of the values on each side of `or` is true

```python
a = 1
b = 0
c = 0

print a and b
print a and not c
print a or b
```

```sh
False
True
True
```

We already know that 1 equals True and 0 equals False. So the first line compares _a_ to _b_ with
the comparison method _and_. It returns False because they to not contain the same boolean value.
For the next line, we compare _a_ to the inverted value of _c_ using the same comparison operation. 
Both are True, so the comparison returns True. In the last line, we compare _a_ to _b_, 
however this time there is another comparison operator, _or_. As one of the values are True, the 
_or_ comparison returns True. 

## Conditional statements (If statements)
In our daily life we need to make decisions all the time. __If__ it's cold outside then I'll
grab a jacket, __otherwise__ I'll use a T-shirt. __If__ it's a weekday then I go to work, __otherwise__
I chill at home. It's not that simple in the real world, since there can be lots of answers to different
questions. The essence here is that we evaluate conditions and act upon the result.
An if statement checks whether a value or comparison is `True` or `False`. The code block inside the
if statement gets executed if the result of the comparison is `True`.
Indentation is what tells the interpreter which code belongs to the if statement.
Most people indent using four spaces, but some like to indent using tabs.

An if statement consists of three parts:

1. `if` - Can be used alone or extended with `elif` or `else`. It checks a comparison. If the comparison is `True`, the indented code block inside `if` is executed.
2. `elif` - Works the same way as `if`, but has to come after an `if`. If `if` is `False` then go to `elif`, if it is present.
3. `else` - If all tests above are False, then execute code block inside of `else`.

Check out this figure to understand the flow of if statements:

![If statement](https://storage.googleapis.com/tghack-public/iftest.png)

```python
lst = ['x', 'y', 'z']
a = 0
b = 1

if a:
    print a
elif a > 4:
    print 'a is greater than 4'
elif 'y' in lst and b:
    print ', '.join(lst)
else:
    print a - b
```

```sh
x, y, z
```

By now, you might be comfortable with the boolean variables and understand why we 
get the output, but we will explain it either way.  First, we initialize three variables, the 
list _lst_, _a_, and _b_. Then we get to the if-statement. The `if` checks whether _a_ 
is True. It is not, so we skip the indented part and continue to the `elif`. It checks if _a_ 
is larger than 4, but it is not. So we move on to the next `elif`. This one returns True 
because both the character _y_ is a part of the list and _b_ is True. Notice the comparison 
operation in the middle. As it returns returns True, we execute the indented code. The
indented code returns a string containing each element of the list with a comma between 
them, hence `x, y, z`.

## Loops

Every line of code in a Python script gets executed sequentially. Sometimes we want
to execute a block of code several times. For example if we want to make a countdown
timer, using a loop is a smart choice. Inside of a loop we can subtract `1` from the current
count and wait `1` second. This way we don't have to write the same code multiple times.
There are two types of loops: `for` and `while` loops.

Loops use indented code blocks just like if statements. The indented code is what is
going to get repeated until the loop is done iterating.

### For loops
For loops iterate over a given sequence. Check out this example:

```python
for number in [2, 4, 6, 8]:
    print number
```

The code in the snippet above outputs:

```sh
2
4
6
8
```

The next example is pretty straightforward. Instead of specifying every number in a sequence there
is a function called `range` or `xrange` (for Python 2.7). With `range` we can specify a range of
numbers to iterate over. The `range` function takes 3 parameters (_start_, _stop_, _step_), but only 1
is required. If you only use 1 parameter, the number you choose becomes _stop_, the _start_ parameter defaults to 0
and _step_ defaults to 1. The sequence of numbers then increment by 1 and will range from
`0` to `[your number] - 1`. That is because all numbers are checked that they are less than (`<`) _stop_.
The last parameter, _step_, specifies how many steps at a time the number will increase by.

```python
 # Prints 0, 1, 2, 3, 4, 5
for x in xrange(6):
    print x

 # Prints 8, 9
for x in xrange(8, 10):
    print x

 # Prints 2, 4, 6, 8
for x in xrange(2, 10, 2):
    print x
```

### While loops
While loops repeat as long as a certain boolean condition is met. When the condition is `False` the
`while` loop stops. Let's take a look at an example:

```python
count = 0
while count < 8:
    # In Python 2.7, if a print statement ends
    # with comma, it won't print a newline.
    print count,
    count += 1
```

```bash
0 1 2 3 4 5 6 7
```

This script prints a count for every iteration of the loop. First we set the `count` variable
to `0`. Then we have a `while` loop that does two things. It prints `count` and increases `count` by `1`. For every iteration
the program checks if the value of `count` is less than `8`. If that boolean condition is met, it enters the 
indented code and executes it. Afterwards, it goes back to check whether the boolean condition is still 
met. And so it continues until the boolean condition returns False. In our case, the condition is `False` 
when the value increases to `8`, 
and the loop stops.

<details>
  <summary>Have you heard about infinite loops or endless loops?</summary><p>
  Infinite loops, also called endless loops, are loops that never stop. They just run and
  run, and never get to continue running the code after the loop. These loops either 
  don't have any terminating condition, have a condition that can never be met, or 
  they have a condition that makes the loop start over.

  Following is an example of an infinite loop. The condition is always True, and nothing can
  ever make it False. The script will print `Infinite Loop` until manually stopped by the user:

  ```python
  while True:
      print("Infinite Loop")
  ```

  (If you actually run this code, press Ctrl+C to stop the script.)

  Read more about infinite loops [here](https://en.wikipedia.org/wiki/Infinite_loop).
</p></details>

<br>

### "Break" and "continue"
A last important thing to know about before you start creating loops is the `break` and `continue` statements.
`break` is used to exit a loop before it is supposed to finish. On the other hand `continue` is used to skip
the rest of the block inside the loop and then continue on the next iteration of the loop.

```python
 # Prints 5, 4, 3, 2 and breaks loop
countdown = 5
while True:
    print countdown,
    countdown -= 1
    if countdown < 2:
        break
```

```python
for x in xrange(4):
    # Skips printing 2 and continues on the next iteration
    if x == 2:
        continue
    print x
```

The code snippets above output the following: 

```sh
5 4 3 2
```

```sh
0
1
3
```

That was a lot of stuff! Now you've been through _boolean operators_, _if-statements_,
and _loops_. These concepts are essential parts of any programming language, so this is
very valuable knowledge. Hope you didn't lose your tinfoil hats!

In the next part, we will tackle functions, classes, and modules. Good luck!

<br>

# Functions, classes and modules
For today's lesson you will learn about functions, classes and modules. 
We all like to be lazy, right? If something has been done before, why 
should you do it again? That is what functions, classes and modules cover
in Python.

[![Lazy wizard](https://storage.googleapis.com/tghack-public/lazy.jpg)](https://www.flickr.com/photos/ad7m/5574061393)

<br>

## Functions
A function is a piece of code called by name. The same code snippet can be
used multiple times in other places of the script. We tend to use functions
so we can write less code and make the code cleaner without removing any functionality.
That is smart, right? Cleaner code makes it easier to read what the code does!

Here are a few things you should know about functions:

- __Functions__ are defined using the keyword `def` in Python.

- __Parameters__ that functions need are placed in the parentheses. Parameters are
values we would like to pass into the function when we call it. When the function
is called, the values respectively get stored in the variables defined inside the parentheses.
These variables are only available locally inside of the function scope. If you
don't want to pass any values to the function, just leave the parentheses empty!

- __Indentation__ defines which code is in the scope of a specific function.
Just like `if` statements or loops. No new magic here!

- A __description__ of the functions can be placed on the first line inside of
the function block. Either single or triple quotes should be used (triple quotes for multiline
description). This string is called a _docstring_.

- `return` exits the function and returns the value that comes after `return`. A function does not have
to return anything if not needed, so this is optional.

Let's try out these new things we have learned! Here we create a function that merges two lists,
sorts the content and then returns the result as one single list.

```python
def merge_and_sort_lists(list1, list2):
    """Merges two lists and sorts the result"""
    outlist = list1 + list2
    outlist.sort()
    return outlist

magical_list = ["Gnome", "Elf", "Griffin", 4]
mythical_list = [1, "Dragon", 3, 8, 4, 9]

print merge_and_sort_lists(magical_list, mythical_list)
```

We call `merge_and_sort_lists` using two lists as parameters and print out the
return value, which is a single list:

```sh
[1, 3, 4, 4, 8, 9, 'Dragon', 'Elf', 'Gnome', 'Griffin']
```

Great! Instead of writing the same code for merging lists every time, 
we can just call the function again using different parameters!

### Default values for parameters
When a function is declared, a default value can be added to each parameter.
This value will be used if this parameter is not specified when the function
is called.

```python
def sum(num1=0, num2=5, num3=3):
    print "The sum is: %d" % (num1 + num2 + num3)

sum(3, 4)   # num1 = 3, num2 = 4, num3 = 3
sum(num3=0) # num1 = 0, num2 = 5, num3 = 0
```

We can specify only 2 parameters, and the third one will use its default value:

```sh
The sum is: 10
The sum is: 5
```

As you can see above, you may also pass a value for a specific parameter using 
the parameter name.

## Classes
Python is an objective oriented programming language. Have you heard about this
term before? Oh well, you are in for a treat! Almost everything in Python is an
object. An object has its own attributes and methods. What are attributes and methods?
A method is almost the same as a function, but the difference is that it is
associated with an object, and can operate on data contained within the class.
Attributes however, are like variables associated with an object.

A class can be explained as a _blueprint_ for creating objects. We can think of
it as a collection of default functions and variables that all objects based on
this class will inherit. In other words, an object is an instance of a class, and
there can be multiple objects based on the same class. So what does all of this mean?
Let's look at an example to understand it better:

```python
class Student:
    """Info about student at School of Wizardy"""
    first_name = ""
    last_name = ""
    age = 0
    house = "Unknown"
    classes = []

    def info(self):
        print "Name: %s %s" % (self.first_name, self.last_name)
        print "Age: %d" % self.age
        print "House: %s" % self.house
        print "Classes: %s" % ', '.join(self.classes)


new_student = Student()
new_student.first_name = "Mike"
new_student.last_name = "Koriander"
new_student.age = 16
new_student.classes = ["Python", "Pwntions", "Defense against dark arts"]
new_student.info()

print "----"

another_student = Student()
another_student.first_name = "Jacob"
another_student.info()
```

The script prints information about students:

```bash
Name: Mike Koriander
Age: 16
House: Unknown
Classes: Python, Pwntions, Defense against dark arts
----
Name: Jacob
Age: 0
House: Unknown
Classes:
```

Wait, hold on, that's a lot of code! Let's break it down. First we take a look at the `class`.

1. First we declare a class called `Student` and give it a few variables (attributes) with default values.
2. We add a method to the class called `info`. This method prints out all of the info about
the student using the previously defined attributes. But what is `self` doing in this function?
Well, `self` represents the instance of the class. By using the `self` keyword we can access
the attributes and methods of the class.
3. We initialize a new variable `new_student` which becomes a new instance of the `Student` class
4. The next step is to add some info about the student. We can access the attributes of the object by
using what is known as dot notation: First the name of the object followed by a `.`, then the name of the attribute.
It's the same for methods as well, but don't forget to add parentheses at the end of the method name to
call it. Just like any other regular function.
5. The `info` method gets called and prints out all of the info.
6. Just to show you there can be multiple instances of a class, we create a new `Student` object called
`another_student`.
7. `another_student` only has its `first_name` set before we print out the info.

Let's talk about a last thing before we continue to the __modules__ section of this lecture.
There is another, more clean way, to do the same thing as the script above. All Python classes have a
reserved method called `__init__`. It is known as a _constructor_ and gets called whenever we create
a new instance of the class. Now we have the opportunity of setting all of the `Student` attributes
above in a single operation.

```python
class Student:
    """Info about student at School of Wizardy"""
    first_name = ""
    last_name = ""
    age = 0
    house = "Unknown"
    classes = []

    def __init__(self, first_name="", last_name="", age=0, house="Unknown, classes=[]):
        self.first_name = first_name
        self.last_name = last_name
        self.age = age
        self.house = house
        self.classes = classes

    def info(self):
        print "Name: %s %s" % (self.first_name, self.last_name)
        print "Age: %d" % self.age
        print "House: %s" % self.house
        print "Classes: %s" % ', '.join(self.classes)


new_student = Student(first_name='Michael',
                      last_name='Koriander',
                      age=15,
                      classes=["Python", "Pwntions", "Defense against dark arts"]
              )
new_student.info()
```

We can see that we get the same output:

```bash
Name: Michael Koriander
Age: 15
House: Unknown
Classes: Python, Pwntions, Defense against dark arts
```

## Modules and packages
We have now arrived at the last section of this lecture. Let's learn about _modules_ and _packages_!

- A _module_ is actually just a Python file containing one or more classes or methods.
- A _package_ can contain multiple modules

Think of _modules_ as files and _packages_ as folders.

Modules and packages can be imported into your own Python scripts. They can be really useful
and there are lots of modules/packages with different functionality to help you solve problems.
How do you use these modules? By importing them into your script.

- `import my_module`
- `from my_package import my_module`
- `from my_module import my_class`
- `from my_package.my_module import my_class`
- `from my_module import *` (`*` imports all classes from a module)

There are lots of ways to import stuff based on if you want to import a module, package, class
or just everything from a specific package or module.


There are three types of modules/packages:

- __Local files and folders__. By organizing code with different functionality into files, it's easier
to go back and make changes to the code. Instead of scrolling through a single large file, you
can rather open the file containing the code you want to edit.
- __Built-in__ modules in Python that you can import right away.
    - [time](https://docs.python.org/2/library/time.html?highlight=time#module-time),
	  [os](https://docs.python.org/2/library/os.html?highlight=os#module-os),
	  [sys](https://docs.python.org/2/library/sys.html?highlight=sys#module-sys),
	  [random](https://docs.python.org/2/library/random.html?highlight=random#module-random),
	  [re](https://docs.python.org/2/library/re.html?highlight=re#module-re),
	  [math](https://docs.python.org/2/library/math.html?highlight=math#module-math),
	  [datetime](https://docs.python.org/2/library/datetime.html?highlight=datetime#module-datetime),
	  etc.
- __Third party__ modules made by different developers uploaded to [pypi.org](https://pypi.org)
    - [pwn](https://pypi.org/project/pwn/),
	  [requests](https://pypi.org/project/requests/),
	  [PyCrypto](https://pypi.org/project/pycrypto/),
	  [scrapy](https://pypi.org/project/Scrapy3/),
	  [scapy](https://pypi.org/project/scapy/),
	  [numpy](https://pypi.org/project/numpy/),
	  etc.


When the `import my_module` runs, the Python interpreter will first look for a file
in the same directory the script was executed from. The name of the file should be the same
as the module appended with a _.py_ prefix.
In our case it will try to look for _my\_module.py_. If Python finds a matching file, it will import it.
If not, it will continue to look for third party or built-in modules.

Example using imports:

```python
import os
from datetime import datetime

current_directory = os.getcwd() # Returns file path of current directory
files = os.listdir(current_directory) # Get list of files

print "Date", datetime.now()

for file in files:
    print file
```

Prints today's date using the [datetime](https://docs.python.org/2/library/datetime.html) module,
and lists files using [os](https://docs.python.org/2/library/os.html)

```bash
Date: 2019-01-19 20:51:01
listfiles.py
The_greatest_wizards.pdf
elixir_recipe.txt
secret_book_of_spells.pdf
```

As you can see, modules are very useful for us! Imagine if we had to write our
own classes and functions that could list files or print out the date. We would have
spent a lot of time, for sure! You will learn about a few modules later that will make
it easier for you to solve the challenges awaiting...

This is the end of the lecture about functions, classes and modules. Good job getting 
all the way through! You are in for a treat for the next (and last) lecture by 
Professor Zup, where you are presented with file handling and exception handling 
of files. 

<br>

# File handling, context managers and Exceptions
Welcome to the very last lecture of the _Pythontongue_ class! Well done getting through
all the previous lectures, I am sure this one will be a breeze. We are going to talk about
the use of files in _Python_ scripts, _context managers_ to better handle resources,
and how to deal with errors (_Exceptions_) when something unexpected happens.

## File handling
Let's jump straight into file handling. File handling is what we call actions such as
opening, modifying and closing files. An important word to learn when handling 
files is `mode`. The mode is specified in order to know what is allowed to do with 
a file. In other words, it specifies which permissions the Python script have when 
opening it. Take a look at the following snippet, and read further explanations 
underneath. 

```python
brain = open('/human/brain', 'w')
brain.write(lecture)
brain.close()
```

Files on your local system can be opened using the `open` function in _Python_.
`open(file, mode)` opens the file `file` in mode `mode`. We now have a _file object_
we perform different operations on, like reading, writing, and seeking. _File objects_
contain methods and attributes that can be used to manipulate or collect information
about the file.

Here are the different modes of opening files:

- `'r'` = read
- `'w'` = write
- `'a'` = append
- `'b'` = binary

If the file is opened in _read_ mode, we can only read the contents of the file, and
not write anything to it. However, in _write_ mode we can write data to the file, but not
read anything from it. _append_ is the same as write, but you append data to the file
instead of overwriting it like regular _write_ does.

There is also a way to combine modes together:

- `'rb'`  = read binary file
- `'r+'`  = read and write
- `'rb+'` = read and write binary file
- `'wb'` = write binary file
- `'w+'` = write and read
- `'wb+'` = write and read binary file
- `'ab'` = append binary file
- `'a+'` = append and read
- `'ab+'` = append and read binary file

The difference between `'r+'` and `'w+'` is that `'r+'` does not overwrite
the file. The latter, however, overwrites the file if there is something in it already.
If the file does not exist, `'w+'` will create a new file, while `'r+'` will have trouble
opening it.

__Useful methods:__

- `.tell()` - Tells current position in file object
- `.seek(byte, mode)` - Jumps _byte_ number of bytes into the file from position _mode_
    - 0 = From beginning of file
    - 1 = From current position
    - 2 = From end of file
- `.read(x)` - Reads _x_ number of bytes from the file. If _x_ is not defined,
  it reads the whole file.
  ```python
  f = open('files/secrets.txt', 'r') # Open file in read mode
  content = f.read() # Read the whole file
  print content
  ```
  This snippet prints the content of the file. We got all of the content by using `.read()`
  ```sh
  Hey, don't look at my secrets!
  ```
- `.write(string)` - Writes the string _string_ into file
  ```python
  f = open('files/new_secret.txt', 'w')
  f.write('Since you saw my secrets, I have to make a new one...')
  ```
- `.close()` - Closes the file to free up resources for your computer to use elsewhere.
  Remember that you can't use the file object anymore after you have called `close()`
  on it.
- `.closed` - Returns `True` if the file is closed and `False` if it's not.
  ```python
  print "Closed:", f.closed
  f.close()
  print "Closed:", f.closed
  ```
  Look what happens after we `close()` the file `f`:
  ```sh
  Closed: False
  Closed: True
  ```

These are probably the methods for file objects you are going to use the most.
There are several more methods that we haven't talked about yet. We won't go
through all of them, but we can show you a few more.

Professor PewZ and I, Zup, have even more tips for becoming a great file handler!
Often you want to create a loop that does something to every line in a file.
A smart thing to do is to use one of these methods:

- `.readline()` - Read a single line from the file and return it as a _string_
- `.readlines()` - Read every line in the file and return them as _strings_ in a list


## Use a context manager and forget about `.close()`

It's not always easy to remember to close our file when we are done with it.
This is because it frees up system resources to be used elsewhere. In Windows
the default behavior is to prevent opening files that
are already opened by someone else. To access a file opened by your script, one
has to wait for your script to finish, if you haven't already closed it. Though this
is only an issue for programs that executes for a long time, it's best practice to
always close your files when you don't need them anymore.

Using a _context manager_ makes things easier, because it automatically closes
the file for us when we are done with it. Instead of doing `f = open(...)`
we can instead use the `with` statement:

```python
with open('list_of_spells.txt', 'r') as f:
    for spell in f.readlines():
        print spell

print "\nFile is closed: %s" % f.closed
```

The above snippet opens a list of spells using the _context manager_:

```sh
Riddikulus
Obliviate
Sectumsempra
Alohomora
Lumos
Expelliarmus
Wingardium Leviosa

File is closed: True
```

As you can see the _context manager_ closed our file for us! We can only use our file
object `f` inside of the indented `with` block. The `as` keyword can be used together
with the `with` statement in order to reference the file object using a name.

<br>

## Exception handling of files
Wait a minute! There is something wrong with one of my _Python_ scripts!

```python
with open('unknown_file.txt', 'r') as f:
    data = f.read()
    print data
```

Let's open `unknown_file.txt` and read its content:

```bash
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
IOError: [Errno 2] No such file or directory: 'unknown_file.txt'
```

Can you spot why my script does not work properly?

Yes that's right! My script tries to read a file that does not exist, and
it is causing an _exception_. When a serious _exception_ is raised, your program
usually crashes and won't execute any more code. This is bad for us,
because we want to print out some data, right?

So, how can we tell our program to not crash when an unexpected _exception_ occurs?

- `try` - Try to execute code. A critical operation which can raise an exception
  is placed inside the `try` clause.
- `except` - Must follow a `try`. If an _exception_ occurs inside of the `try` clause,
  run the code in the `except` clause. The code in the `except` clause should
  handle the _exception_ that occurs!
- `finally` - Must follow a `try` or an `except`. Execute code regardless
if an _exception_ was raised or not

The `try` and `except` flow looks like this (`pass` is just a keyword that does nothing):

```python
try:
   # do something that may raise an _exception_
   pass

except IOError:
   # handle IOError exception
   pass

except (ZeroDivisionError, ValueError):
   # handle multiple exceptions
   # ZeroDivisionError and ValueError
   pass

except:
   # handle all other exceptions
   pass

finally:
   # Do something more
   pass
```

For files in _Python_, an exception can for example occur when:

- `open(filename, 'r')` - The file _filename_ does no exist and mode is _read_
- `read()` - You get disk error, network is down (if you are accessing a file remotely)
- `seek()` - You "jump" to outside of the file area. For example jumping to the 64th byte
  when the file is only 36 bytes long.

Let's try to make a handler for the _exception_ we saw in the example above!

```python
try:
    f = open('unknown_file.txt', 'r')
    f.close()
except IOError as e:
    print "IOError: [Errno {number}] Help! {string}: {file}"\
          .format(number=e.errno, string=e.strerror, file=e.filename)
finally:
    print "Done!"
```

This example prints our own message when the _IOError_ exception occurs:

```python
IOError: [Errno 2] Help! No such file or directory: unknown_file.txt
Done!
```

The script will no longer exit (crash) earlier than expected if `unknown_file.txt` does
not exist.

----

<br>

## Class dismissed!

Class dismissed! We are done with the __file handling__ lecture!
Professor PewZ will take over from now on. He will teach you more about
_Python_ modules and how you can solve _CTF challenges_ using this awesome
and magical language.

I hope that you had a great time going through all of
these lectures and are motivated to start writing some code on your own!

For more info about the _Python_ language, please check out the
__documentation__ where you can find info about every function, method, variable
type and so on:

[Python2 Documentation](https://docs.python.org/2) |
[Python3 Documentation](https://docs.python.org/3)


# Using the pwn module to solve CTF-challenges

Now, dear witches and wizards, let's get started on solving some CTF challenges!
I hope you had fun going through the Python tutorial, and that you are ready to
push your skills even further.

Many CTF challenges require you to connect to some mystical service to show off
your magical abilities. Thankfully, there are libraries available to help us
communicate with services more easily. Good luck, and have fun!


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
This includes connecting to a remote service, sending and receiving
data, and manually interacting with the service. pwntools has a lot of
functionality not covered by this short tutorial, so if you want to know more,
take a look at some of the resources at the end of the tutorial.

All the code snippets in the following sections should be saved in a text editor
of your choice. You can then run the script by using the `python2` command from
the terminal.

We will solve two different tasks using pwntools in this tutorial. Good luck!

### Installation of pwntools
In order for us to use pwntools, we have to install it first. The following
example works on Debian-based distributions. These are Linux distributions based
on Debian, and includes Ubuntu, Lubuntu, Xubuntu, Debian, and others. To install
the library, open the terminal on your machine, and enter the following
commands:

```bash
$ sudo apt-get update
$ sudo apt-get install python2.7 python-pip python-dev git libssl-dev libffi-dev build-essential
$ sudo pip install --upgrade pip
$ sudo pip install --upgrade pwntools
```

If you have trouble installing pwntools on your machine, please don't hesitate
to ask for help on the TG:Hack Discord!

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

### Echo Chamber
You should be ready to tackle the Echo Chamber challenge now. Good luck, and
have fun! You can find the challenge under the n00b category at
[tghack.no](https://tghack.no).

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

### The Calculator
Equipped with a few functions from pwntools and the corresponding documentation,
you should be ready to test your newfound skills with mythical languages against
our calculator challenge. You can find the challenge under the n00b category at
[tghack.no](https://tghack.no).

### Resources
[pwntools docs](https://docs.pwntools.com/en/stable/)

# Using Crypto Modules in Python

Cryptography can be a difficult topic, and not all programming languages have
good support for crypto libraries to make scripting of cryptography related
tasks easier. Fortunately, Python has some nice libraries that we can use to
solve CTF tasks [pertaining](http://lmgtfy.com/?q=pertain) to cryptography.
In this tutorial, we will be using
[pycrypto](https://github.com/dlitz/pycrypto). This library has support for all
the functionality we need for basic crypto tasks.

### Installation of pycrypto
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

### Numbers or Bytes?
To practice, we have set up a task called `Numbers or Bytes?` in the n00b
category.  
The task asks you to convert between numbers and byte strings. You will have to
do this 1000 times to get the flag. If you haven't checked out the previous
chapter in this tutorial, you should do that first, since using pwntools will
help you a lot when solving this challenge.


### Hash Functions
A hash function is a function that takes an arbitrary amount of data as input,
and outputs a fixed amount of data. The function can take a whole file of many
gigabytes, or a small program of a couple of megabytes. Even a single character.
The output, however, will always be the same size. In addition, the output will
always be the same. Just a slight change in output will cause the output to be
dramatically different. See the following example, where we have the MD5 hashes
of `foobar123` and `foobar124`:

```bash
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

### Let's Hash it Out
We created a task for you that lets you try out different hash functions in
Python. The task is called `Let's Hash it Out`, and you can find it in the n00b 
category at [tghack.no](https://tghack.no).
The goal is to hash different strings using several hash functions. Like many
of the other n00b tasks, you will have to do this 1000 times to get the flag.
Good luck!

<br>

### Resources

* [pycrypto](https://github.com/dlitz/pycrypto)
