# Simple encoding

_Mr. Josefsson is a magician at Unix Schoole Of Witchcraft n’ Wizardry. He is
old and forgetful, so he wants to write down his spells on pieces of paper.
There is no way known to wizard to notate the hand waving involved in spell
casting, so he is in a bit of a pickle. What Mr. Josefsson needs is a way to
encode hand waving into text; he needs an encoding scheme. He decides that
waving upwards should be notated as “up”, and downwards waving should be
written as “down”. Likewise he can write “left”, “right” and “flick” for other
movements._


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
</details><br>

