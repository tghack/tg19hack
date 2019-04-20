# Writeup - Crypto n00b2

We are given a flag, but all the letters are wrong.
It might have been encrypted with a shift cipher. How
can we find the correct shifting value to get the flag?
We know that all flags start with `TG19`. What's the shift
value to go from `OB19` to `TG19`? 5! Then if we shift all
letters with 5, we get the flag:
```
TG19{the_most_basic_type_of_encryption}
```
