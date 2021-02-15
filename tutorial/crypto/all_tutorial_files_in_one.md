# History of Cryptography

Hello, aspiring wizards and witches! I can see you are 
eager to learn all the secrets of the wizarding world. 
Yes, secrets! That is what this class is all about! Have
you ever wondered how the wizarding world have stayed hidden
from the muggles for so long? Or how the Aurors are able to
communicate without dark wizards knowing? Then you have come
to the right place, for here we will unravel some of
these well kept secrets.

I am Professor Chabz, and together with Professor nic0, I will
give you an introduction to the art of cryptography. Our assistant,
Mr Josefsson, will help us throughout the class to illustrate
problems cryptography can solve. A fair warning before we start: 
cryptography is not for the faint of heart! But persevere and a
master of secrets you can become. 

## Agenda of the class
This class consists of three parts. First we will show you how
to do basic _encoding_, then we will move on to _shift ciphers_, and
lastly we will teach you stronger cryptography by using the spell _XOR_.

<br>

**Class plan**

| Class topic | Description |
|:-----------:|:-----------:|
| Simple Encoding | You will learn what encoding is and how it can be used. | 
| Shift Cipher | Introducing the concept of secret, you will learn why encoding is not safe and how encryption helps. |
| Stronger Cryptography | You will learn what XOR is and how it can be used to encrypt. |

<br>

## Exams giving magical XP points
There are four exams for this class. At the end of each class, you will 
be presented with a new exam that you might be ready to take. All of the exams 
can be found in the crypto category in the tasks page. Here is a list of the 
exams:

| Exam name | Points |
|:---------:|:------:|
| American Standard Code for Information Interchange | 25 |
| Land of Encoding | 25 |
| Rotarius | 25 |
| Exclusive Magic Club | 50 |

Now you are ready to delve into the world of secrets! 
Good luck, my students!

<br>

# Simple encoding

_Mr. Josefsson is a magician at Unix Schoole Of Witchcraft n’ Wizardry. He is old and forgetful, so he wants to write down his spells on pieces of paper. There is no way known to wizard to notate the hand waving involved in spell casting, so he is in a bit of a pickle. What Mr. Josefsson needs is a way to encode hand waving into text; he needs an encoding scheme. He decides that waving upwards should be notated as “up”, and downwards waving should be written as “down”. Likewise he can write “left”, “right” and “flick” for other movements._


Encoding is used in the real world to change information that cannot be
properly written as text, into text. Binary information (0's and 1's) are the
most common type of data to be encoded, and for that we have an *encoding scheme*
called Base64.

> A *scheme* is just a set of rules, and the rules of Base64 dictates how any
> sequence of bits should be written as symbols.

The binary text `01110100 01100111` are for instance written as `dGc=`. No one
goes around remembering that, though! We use tools to do these conversions. The
symbols we use in base64 are
`ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/` so if
something is encoded with Base64, these are the only symbols you will see.
They sometimes end with equal signs (`=`) because Base64 encoded
strings must have a length divisible by 4, and equal signs are just added to
the end to make that happen.

> It is common for ciphers and encoding schemes to require data of a given
> length. When there is not enough data, we need to increase the length. This
> process is known as
> [padding](https://en.wikipedia.org/wiki/Padding_(cryptography))


> Theres a lot to say about encoding schemes, binary notation and other
> subjects mentioned here. Feel free to google for stuff you don't understand.

Now that you know what encoding means, you should try the first and second n00b
crypto tasks!


<details><summary>More on Base64</summary>
Base64 is an encoding scheme with 64 characters, a to z, A to Z and 0 to 9. It
is commonly used to transfer media, like images, over a transport that is
designed to deal with text. This is to ensure that data remains intact without
modification during transport. HTTP is a transport protocol, but Facebook chat
is also a kind of transport because you transport messages from one place to
another. So if you want to send raw image data over Facebook chat, it would
look like garbage, and some data might get lost, but if you Base64 encode the
data, then the person on the other end could Base64 *decode* the data, and the
data would be correct.  It is generally accepted that we choose characters from
a to z, A to Z, 0 - 9, and a couple of symbols, so you if you decide to use
Base32, that would mean that you only use 32 characters of that. For base32 its
A-Z and 2-7 for some reason.
</details>

<br>

# Shift cipher

_One day when Mr. Josefsson was walking down one of the corridors, he noticed some students practising wand movements. “Why are they standing here in the hallway…?”, Joseffson pondered, “But wait a minute… It can’t be…”. He walked calmly over to the students. “Practising hard, I see.” The students jumped. “Oh, uuh, yes, Professor,” one of them piped up. “We have to go to our next class. See ya!”, another one said and they rushed off. “Next class? The next class starts in half an hour… and those wand movements looked a bit familiar. Could it be…?”_

Looks like someone managed to find Josefssons notes, with his wand movements
encoded as text! This is a problem with encoding: you have not secured your
information because the translation of data is public information. This means
that anyone can decode your information with little effort. To avoid this and
secure your data properly you have to use encryption, which means that we
must introduce some kind of secret into the formulae. One of the earliest and
simplest examples of encryption is the **shift cipher**. Instead of using a public
mapping to some kind of language or alphabet like we did with `base64`, we
construct a *secret* alphabet. With shift cipher we choose a random number
that we use to shift the original text into other letters. By introducing this
secret part, we have encrypted the text, not just encoded it.

![Shift cipher illustration](https://storage.googleapis.com/tghack-public/shift_cipher.svg)

The image shows an example where the secret shift is -3. The text `wave right`,
when shifted three times backwards in the alphabet, becomes `txsb ofdeq`. That's it!
So it's not a very strong form of encryption, but it's a start.

With your newfound knowledge you should be well prepared to try and solve the
third crypto task!

<br>

# Stronger cryptography

_Even after Mr. Jonsson started encrypting his notes, students were able to decrypt his messages. The encryption method was too simple, too easy to figure out. “I need something stronger”, he thought. “A-ha!”, exclaimed Jonsson, “I will use XOR cipher! Now I only need a key…”._

The shift cipher we saw in the previous tutorial is not used to secure
information anymore. This is because it does not provide the cryptographic
security required by todays systems. Simply put, it is easy to break shift
ciphers. XOR cipher is harder to break, and Jonsson's messages will remain
secret longer with this method.

XOR cipher uses a secret piece of text, which we call the *key*. This key can
be used to "lock" a message that we want to keep hidden, like when you lock
your front door to keep people out. One big difference between door locks and
cryptography, though, is that just having the key is not always enough: you
sometimes also need to know **how the lock itself works**, because there are
infinitely many ways of encrypting data.

The keys in the previous tutorial were numbers, indicating a shift in the
alphabet. If you know the encrypted message is `rflnh`, and you know the key is
`5`, you still need to know that the "lock" is the shift cipher.  This time we
are switching out the lock with something we call XOR'ing, which is harder to
break than shift cipher. It is built on a simple mathematical function, the one
that gives it its name.

> When we say that one encryption algorithm is harder or stronger than another
> one, we generally mean that it takes more time and/or computing power to
> recover the message *when we don't know the key or the message*, even if the
> steps for doing so may be simple.

You may know that a function, in mathematics and in programming, is just a list
of steps for calculating some values. Some functions, like plus (`+`), need two
numbers to work, and it gives us the sum of those two numbers. The numbers we
choose are called *arguments*, or *parameters*, and they determine what value
we get at the end. `XOR` is like `plus`: it takes two numbers and gives us a
result, but it only works for two numbers: `0` and `1`. The rule is simple
enough: if both arguments are the same, the answer is `0`, and if they are
different, the answer is `1`.

| A | B | Output |
|:-:|:-:|:-:|
| 0 | 0 | 0 |
| 0 | 1 | 1 |
| 1 | 0 | 1 |
| 1 | 1 | 0 |

This may look strange, and even useless, but this function has a very important
property: If you have a number `n`, either `1` or `0`, and you XOR it twice
with a number `x`, then you have the same number again. So `(1 XOR 0) XOR 0 =
1`, `(1 XOR 1) XOR 1 = 1`, or more generally `(n XOR x) XOR x = n`.

But how on earth can we use this for anything? Well, first of, let's talk about
something we mentioned in the first cryptography tutorial. We talked about
ASCII, which is the name of the document that says how text on computers is
represented in `1`s and `0`s. `a` is written as `01100001`, `b` as `01100010`
and so on.  When we write text like this, as its binary representation, we can
use it in our XOR function!

Okay, and the second thing is that because the XOR function can be used twice
to get the same result back, we can use our key both for encrypting *and*
decrypting a message.

> Fun fact: The XOR cipher is a *symmetric* cipher, because we use the same key
> for encryption and decryption. There are also
> [*asymmetric*](https://en.wikipedia.org/wiki/Public-key_cryptography)
> ciphers, where we have one key for encryption and one for decryption!

Time for an example. Our message is `hi` and the key is `c`.


|   |   |   |   |   |   |   |   |   |
| - | - | - | - | - | - | - | - | - |
| h | 0 | 1 | 1 | 0 | 1 | 0 | 0 | 0 |
| c | 0 | 1 | 1 | 0 | 0 | 0 | 1 | 1 |
| ? | 0 | 0 | 0 | 0 | 1 | 0 | 1 | 1 |

We end up with `00001011`, which does not translate to a letter, but that is
fine. The important property of XOR is that we can use the same key `c` to get
the `h` back:

|   |   |   |   |   |   |   |   |   |
| - | - | - | - | - | - | - | - | - |
| ? | 0 | 0 | 0 | 0 | 1 | 0 | 1 | 1 |
| c | 0 | 1 | 1 | 0 | 0 | 0 | 1 | 1 |
| h | 0 | 1 | 1 | 0 | 1 | 0 | 0 | 0 |

Check for yourself!

> We won't show `i XOR c` but you can try that yourself!

The key does not have to be a character, it can be any random combination of
`1`s and `0`s, and it can be any length. It can be `11`, `00000001` or
`100111111101010011000000100111100111111111110010001100100`. The longer it is,
the harder it is to guess, and if the message is longer than the key, we just
use the key again.

Here the key is just the bits `01`. Since the ASCII character `h` is eight
bits, we need to use the key 4 times.

|   |   |   |   |   |   |   |   |   |
| :-: | - | - | - | - | - | - | - | - |
| h | 0 | 1 | 1 | 0 | 1 | 0 | 0 | 0 |
|  `01` | 0 | 1 | 0 | 1 | 0 | 1 | 0 | 1 |
| ? | 0 | 0 | 1 | 1 | 1 | 1 | 0 | 1 |

You can play around with XOR on a piece of paper, or in a text editor, or you
can use online tools like [cyberchef](http://tinyurl.com/y465j2r2).
I have prepared a text and XOR'ed it for you. Cyber Chef is very nice, and you
can play around with different encodings and encryption algorithms. What
happens when you change the key? Go ahead and try!

> Tidbit: Do you know where XOR got its name? XOR is a logical operator, which
> is also refereed to as "exclusive or". We also have the "or" logical
> operator, which behaves slightly different. You can read more about logical
> operators [here](https://en.wikipedia.org/wiki/Boolean_algebra#Operations)

----------


This technique is still used as part of bigger algorithms in cryptography
today, and is very relevant if you want to participate in CTFs or if you want
to study and work with cryptography.

If you have read through this tutorial, we recommend that you try the fourth
and last noob crypto task!

<br>

# Outro

Congratulations, you have completed TG:Hack's crypto tutorial! We hope we
managed to give you a small glimpse into the world of encryption and that you
got some helpful tips for solving those horrifying crypto tasks. 

Cryptography is a big topic with many subjects, some easy to use and
understand, and others not. We strongly encourage you to go out and learn more,
even if just to get an overview of what's out there. An essential skill when
participating in CTFs is to be able to find information that helps you solve
the challenges you face. Even just being familiar with some different topics
can make that process easier, therefore we leave you with some resources if
you feel like exploring a bit.


Cryptography video playlist from the brilliant channel Computerphile:
https://www.youtube.com/watch?v=GSIDS_lvRv4&list=PL0LZxT9Dgnxfu1ILW0XnLnq3mb0L5mUPr

A wikipedia page that gives an overview of cryptography:
https://en.wikipedia.org/wiki/Outline_of_cryptography

A great tool that we use ourself when we want to solve other CTF tasks, and
sometimes when we create tasks for you:
https://gchq.github.io/CyberChef/

A huge list of resources both for crypto and other stuff:
https://github.com/apsdehal/awesome-ctf

<br>


An actual course in cryptography filmed and put up on youtube.  As this is
university level material, not everyone will find the whole course informative.
The first few videos is a good introduction that anyone could watch.
https://www.youtube.com/watch?v=2aHkqB2-46k&list=PL6N5qY2nvvJE8X75VkXglSrVhLv1tVcfy
(Don't worry: the image stabilizing effect is only used in the first video)
