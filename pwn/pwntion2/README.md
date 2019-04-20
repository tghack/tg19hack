# Introduction to Pwntions: Stack overflow pt. 2
**Points: 75**

**Author: maritio_o**

**Difficulty: n00b/easy**

**Category: pwn**

---

_"Remember those lectures about Pwnie? Now is your chance to show what you've
learned!"_
    
—Professor maritio\_o

Our beloved house elf is unfortunate to be vulnerable to the
stack overflow pwntions. 

This time, we want you to take the given ingredients and 
brew the pwntion so that his ears turns equally large as the
nose?

Take these files for local pwning, the [source code](uploads/pwntion2.c) and the [binary](uploads/pwntion2).

```
nc pwntion2.tghack.no 1062
```

<details><summary>Tips</summary><p> 

1. The file expects to read a file called `banner.txt`. For the binary to
work locally, you should make a file with that name and put whatever you
would like into it.

2. Read the Stack Overflow pt. 2 section in the
Introduction to Pwntions tutorial to learn about this
type of stack overflow problem.
    </p></details>
