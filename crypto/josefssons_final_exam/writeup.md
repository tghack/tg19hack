# Writeup - Josefssons Final Test
**Points: 75**

**Author: Chabz**

**Difficulty: easy**

**Category: crypto**
___
In this task we are given some binary data
and the keyword `good_luck`. If you have
read the crypto tutorial and solved the n00b
tasks, Mr. Josefsson should be familiar to you.

We know that Josefsson loves XOR, so we try to
use XOR on the binary data with the keyword. This
gives us the following data:
```
DMkfWFbhj29cF3tdlD9pkuDnlOptF2VgmFJ0j19bGFV0HFR9
```
This looks like base64, but decoding it 
gives us some garbage data. But we know that
Josefsson also likes to use shift ciphers. We can try
to apply that here. With some trial and error,
we find that shifting the base64 data with 18 and 
then decoding gives us the flag:
```
TG19{soon_you_are_the_crypto_master}
```
