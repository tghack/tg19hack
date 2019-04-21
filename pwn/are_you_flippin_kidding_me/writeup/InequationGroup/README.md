# Are You Flipping Kidding Me? Writeup

**Author: Frisk**
**Language: EN**

Start TLDR;
Are you Flipping Kidding me was a hard pwn exercise, where one was given a write anywhere primitive which was initially limited to the flipping of only 5 bits. As the executable was only partial RELRO one could flip bits in the Got.PLT table to gain control over the execution and get an unlimited write. From there one could force an infoleak of an address within Libc which allowed one to easily use an onegadget to get a shell.
End TLDR;

[Full Writeup](https://blog.inequationgroup.com/tghackflipping/)
[exploit](./Solve.py)
