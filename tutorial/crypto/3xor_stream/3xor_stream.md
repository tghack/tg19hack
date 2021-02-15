# Stronger cryptography

Even after Mr. Jonsson started encrypting his notes, students were able to
decrypt his messages. The encryption method was too simple, too easy to figure
out. “I need something stronger”, he thought. “A-ha!”, exclaimed Jonsson, “I
will use XOR cipher! Now I only need a key…”.

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
can use online tools like [cyber
chef](https://gchq.github.io/CyberChef/#recipe=XOR(%7B'option':'Binary','string':'00001001'%7D,'Standard',false)To_Hex('Space'/disabled)To_Binary('Space'/disabled)&input=VG8gbWFrZSBhIHBvdGlvbiwgeW91IHdpbGwgbmVlZCB0d28gdGFibGUgc3Bvb25zIG9mIEMsIGFuZCBhIHdpemFyZHMgaGF0Lg).
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
