# Writeup [Enchanted Keys](README.md)

## Task description

**Points: 250**

**Author: zup/kristebo**

**Difficulty: challenging**

**Category: AFK**


## Writeup

*This writeup is based on this [writeup](<https://medium.com/@orik_/34c3-ctf-minbashmaxfun-writeup-4470b596df60>) 
from 34c3. The task was made easier since people are going to write 
the commands manually into a terminal using a keyboard with missing 
keys.*


At the TG:Hack stand, we find a keyboard with missing keys. The only keys 
left on the keyboard are the number keys, `-`, `=`, `}`, `{`, `,`, `.`, `\`, 
`'`, `Alt`, `/`, `Alt Gr`, `F1-F12`, `BACKSPACE`

On the screen is a terminal, so it looks like we must find a way to 
write commands using only a few keys.

So, what can we do using only these characters?

There are multiple ways to solve this challenge, but one thing we can 
do is to use octals instead of characters to write commands. 
This is how to do it in bash:

`$'\137'` - convert octal to a character in string literal. 

We have all of these keys on our keyboard, so it looks like this is 
possible to do!

Let's make a script called `octal.py` in Python that converts a 
command to octal:

```python
#!/usr/bin/env python
import sys

cmd = "find"
if len(sys.argv) == 2:
    cmd = sys.argv[1]

output = "$'"

for c in cmd:
    output += "\\{}".format(oct(ord(c))[1:])
output += "'"

print output
```

```bash
$ python octal.py
$'\146\151\156\144'
```


`$'\146\151\156\144'` is the output we get. When we write this string 
straight into the terminal, it works just like a normal command, 
nice work!

```bash
$ $'\146\151\156\144'
.
./magic_notes
./magic_notes/pranks.txt
./magic_notes/hard_spells.txt
./magic_notes/easy_spells.txt
./magic_notes/dark_spells.txt
./plan_for_the_week.txt
```

Cool! The next step must be to find the `flag.txt` file. We can use 
`find / -name flag.txt` to search through the file system. 

Just replace the command in the script we wrote to convert it to octal:

```bash
$ python octal.py "find / -name flag.txt"
$'\146\151\156\144\40\57\40\55\156\141\155\145\40\146\154\141\147\56\164\170\164'
```

If we try running this command in the terminal, there seems to be an 
issue:

```bash
$'\146\151\156\144\40\57\40\55\156\141\155\145\40\146\154\141\147\56\164\170\164'
bash: find / -name flag.txt: No such file or directory
```

After testing different commands, the issue seems to be the space 
character. To make commands with spaces work we can either 
replace `\40` with a real space:

```bash
$ $'\146\151\156\144' $'\57' $'\55\156\141\155\145' $'\146\154\141\147\56\164\170\164'
/lib/rary_/of_/secret_/flags_/flag.txt
find: '/proc/tty/driver': Permission denied
find: '/proc/1/task/1/fd': Permission denied
[...]
```

or use [Bash Brace Expansion](<https://www.gnu.org/software/bash/manual/html_node/Brace-Expansion.html>):

```bash
$ {$'\146\151\156\144',$'\57',$'\55\156\141\155\145',$'\146\154\141\147\56\164\170\164'}
/lib/rary_/of_/secret_/flags_/flag.txt
find: '/proc/tty/driver': Permission denied
find: '/proc/1/task/1/fd': Permission denied
[...]
```

Since we have don't have a space button, we must use the second 
method. Edit the _octal.py_ script to split the octal string where 
a space occurs, and add commas in between. Also add curly brackets
on each side of the command.

Now we know where the flag is! Since the path is quite long, we can 
_cat_ it using _find_'s exec parameter.

Here is the complete script for converting commands to octal:

```python
#!/usr/bin/env python
import sys

cmd = "find / -name flag.txt -exec cat {} +"
if len(sys.argv) == 2:
    cmd = sys.argv[1]

cmd = filter(None, cmd.split(' ')) # Remove empty items from list
output = "{"

for part in cmd:
    output += "$'"
    for c in part:
        output += "\\{}".format(oct(ord(c))[1:])
    output += "',"

output += "}"
print output
```

Let's print the flag!

```bash
$ python octal.py "find / -name flag.txt -exec cat {} +"
{$'\146\151\156\144',$'\57',$'\55\156\141\155\145',$'\146\154\141\147\56\164\170\164',$'\55\145\170\145\143',$'\143\141\164',$'\173\175',$'\53',}
```

```bash
$ {$'\146\151\156\144',$'\57',$'\55\156\141\155\145',$'\146\154\141\147\56\164\170\164',$'\55\145\170\145\143',$'\143\141\164',$'\173\175',$'\53',}
find: '/proc/tty/driver': Permission denied
find: '/proc/1/task/1/fd': Permission denied
[...]
TG19{unlocking_the_secrets_of_bash}
```

Perfect, we got it: `TG19{unlocking_the_secrets_of_bash}`

