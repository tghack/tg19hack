# Python introduction and variables
In this lesson of the Pythontongue class, we demonstrate how to write
spells properly on script rolls. To begin with, we discuss the different
types of script rolls to write on. Then we move on to how we write something
called _variables_ in the Pythontongue, and what types of variables exists in the
language. We explain what a variable is later on. This is basic knowledge
to make sure you are ready to write powerful spells on your script rolls. 

___A quote from [python.org](https://docs.python.org/2/tutorial/)'s own tutorial___

_"Python is an easy to learn, powerful programming language.
It has efficient high-level data structures and a simple but effective approach to
object-oriented programming. Python’s elegant syntax and dynamic typing,
together with its interpreted nature, make it an ideal language for scripting and rapid
application development in many areas on most platforms"_


<br>

## Several ways to write Pythontongue

<br>

### Python Shell

The simplest way to use Python is the built-in Python shell.
This shell is mostly used to run small amounts of code, and you don't have to create any files to execute this code.

To start the shell type the command `python` or `python2` in your terminal. When you are inside the Python shell, you can type code
that gets executed as soon as you press enter. You have to write the code one line at a time.

To exit the shell you can call the function `quit()`

```
user@tg19:~$ python2
>>> print 'Hello world'
Hello world
>>>
```

<br>

### Straight from the terminal

There is also a way to execute Python code straight from the terminal without entering a Python shell.
Just add a `-c` flag like the example below

```
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
```
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

<br>

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

<br>

#### Text strings (str)
A string is usually a bit of text you want to display to someone, or
"export" out of the script you are writing. Python knows you want something
to be a string when you put either `"` (double-quotes) or `'` (single-quotes)
around the text:

```
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
```
Wizards and Witches
```
It is also possible to use multiplication (`*`) to repeat a string.
```python
print "Lumos" * 4
```
Output:
```
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
```
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
```
WIZARDS AND WITCHES
Wizards and Witches
Wizards or Witches
```

[Check out this link](https://www.programiz.com/python-programming/methods/string) for a list of more string methods.

<br>

__Testing__

Using methods to test whether the string content is as expected.

Tests if the string only contains characters from the alphabet. Returns True or False
```python
print output.isalpha()
```
Output:
```
True
```
<br>

__Converting/Casting__

The method of converting other types into string types.
```python
print str(42) + ' ' + output
```
Output:
```
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
```
Thomas has learned 14 spells this year!
Hailey has learned 8 spells this year!
I know 7 different spells...
```

F-strings were introduced in Python 3.6. This is an even easier way to insert variables or do operations
 inside of strings:
```python
days_left = 25
answer = f"There are {days_left * 5} days left of this semester."
print(answer)
```
Output:
```
There are 125 days left of this semester.
```
<br>
 
---

<br>

#### Integers (int)
Alright, so we just went through a lot of nice functions related to strings. Now, it is time 
to learn about numbers! Every programming language has some kind of way
of doing numbers and math, and this section describes how to handle integers. 
Integers are positive or negative whole numbers with no decimal point. 

<br>

##### Integer operations
- Printing variable type
- Math operations
- Type conversion

<br>

__Printing variable type__

Let's first take a look at integers and create some variables.
```python
wands = 6
owls = 17
frogs = 2
print type(wands)
```
By looking at the output, we can see that the variables are of the type _int_:
```
<type 'int'>
```

<br>

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
```
9
155
25
```

Now, lets trying dividing!

```python
print wands // frogs
```
The operator used above is integer division. Note that `9 // 2` returns an integer and not a decimal number (float):
```
4
```

<br>

__Conversion__

Remember when we converted an integer to a string in the "Text string" chapter? We can also go the other way around:

```python
print 1 + 2 + 3 + int('4') + int('5')

print 1 + 2 + 3 + '4' + '5'
```
As you can see in the example below, we get a _TypeError_ if we don't convert our strings to integers before the addition.
```
15

Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: unsupported operand type(s) for +: 'int' and 'str'
```

<br>

#### Floating point numbers (float)
Floats represent real numbers and are written with a decimal point dividing the integer and fractional parts.
Floats may also be in scientific notation, with E or e indicating the power of 10.
```python
print 3.2e2 == 3.2 * 10**2 == 320

print 5.5 + 19.5
print 9.0 / 2
```
Output:
```
True

25.0
4.5
```
<br>

We can also convert strings or integers to float values:
```python
print float(owls)
print float('56.55')
```
Output:
```
17.0
56.55
```
<br>

#### Lists and Tuples
Lists and tuples are ways to store multiple values in a sequence. Lists can be written as a sequence
of comma-separated values between square brackets. The items in a list does not have to be of the same type.
Tuples are sequences just like lists. The difference between lists and tuples is that lists are mutable
while tuples are immutable. In other words, tuples cannot be changed after initialized unlike lists.
Tuples also use parentheses around the items instead of square brackets.

<br>

##### List operations
- slice
- join
- sort
- pop
- remove
- insert
- append

Slicing makes it possible to get a specific range of items from lists, tuples or custom data structures:
```python
magic = ['cloak', 'wand', 'spellbook']

print magic
print magic[1]
print magic[0:2]
```
Output:
```
['cloak', 'wand', 'spellbook']

wand

['cloak', 'wand']
```

The join operation returns a string from a list. Each item joined gets separated by a chosen separator:
```python
print 'My magic objects are ' + ', '.join(magic) + '.'
```
Output:
```
My magic objects are cloak, wand, spellbook.
```

Here is a tuple. Notice that it's not possible to change an item or add an item to the tuple using the append method. This is
because it is immutable.
```python
magical_numbers = (7, 9, 15, 42, '66')
magical_numbers.append(30)
```
```python
magical_numbers[2] = 12
```
Output:
```
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
AttributeError: 'tuple' object has no attribute 'append'
```
```
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
```
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
```
[('core', 'Phoenix feather'), ('price', 199), ('wood', 'Holly'), ('in_stock', 2)]
```
We get a list of tuples! The tuples contains the key and value of each corresponding item in the dictionary.

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
