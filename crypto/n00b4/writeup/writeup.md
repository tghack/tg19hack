# Writeup - Crypto n00b4

We are given what appears to be a binary string and the text `mother_knows_best`.
Trying to convert the binary string to the corresponding characters only
yields garbage, so it must be encrypted in some way. One of the simplest
ways of encrypting binary is to use the binary operator XOR with a secret
key. Hmm, could `mother_knows_best` be the key? Let's try!

When working on tasks like this, I really recommend using [CyberChef](https://gchq.github.io/CyberChef).
We get the flag by setting it up like this:
![](https://github.com/PewZ/tg19hack/blob/n00b-crypto4/crypto/n00b4/crypto_n00b4.png)

The flag is `TG19{bow_down_to_the_AI_overlords}`.
