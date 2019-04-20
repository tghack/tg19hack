# Writeup - Crypto n00b1

This task gives us a list of numbers that somehow hides a flag.
As we know the flag is made out of letters, we may assume we
have to find a way to convert the numbers to letters. One of
the most common ways to do this is called [ASCII](https://en.wikipedia.org/wiki/ASCII).
By looking at the ASCII encoding table (`man ascii` in the terminal
or find it online), we can map the numbers to their corresponding
character.

Do this for the numbers given in the task and the 
flag appears: `TG19{ASCII_and_you_shall_receive}`.
