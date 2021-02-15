# Functions, classes and modules
For today's lesson you will learn about functions, classes and modules. 
We all like to be lazy, right? If something has been done before, why 
should you do it again? That is what functions, classes and modules cover
in Python.

[![Lazy wizard](lazy.jpg)](https://www.flickr.com/photos/ad7m/5574061393)

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
```
[1, 3, 4, 4, 8, 9, 'Dragon', 'Elf', 'Gnome', 'Griffin']
```

Great! Instead of writing the same code for merging lists every time, 
we can just call the function again using different parameters!

<br>

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
```
The sum is: 10
The sum is: 5
```
As you can see above, you may also pass a value for a specific parameter using 
the parameter name.

<br>

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
```
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
```
Name: Michael Koriander
Age: 15
House: Unknown
Classes: Python, Pwntions, Defense against dark arts
```

<br>

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
```
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
