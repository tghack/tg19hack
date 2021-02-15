# File handling, context managers and Exceptions
Welcome to the very last lecture of the _Pythontongue_ class! Well done getting through
all the previous lectures, I am sure this one will be a breeze. We are going to talk about
the use of files in _Python_ scripts, _context managers_ to better handle resources,
and how to deal with errors (_Exceptions_) when something unexpected happens.

<br>

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
<br>

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
  ```
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
  ```
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

<br>

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
```
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
```
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
