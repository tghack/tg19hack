# Shift cipher

_One day when Mr. Josefsson was walking down one of the corridors, he noticed some
students practising wand movements. “Why are they standing here in the
hallway…?”, Joseffson pondered, “But wait a minute… It can’t be…”. He walked
calmly over to the students. “Practising hard, I see.” The students jumped.
“Oh, uuh, yes, Professor,” one of them piped up. “We have to go to our next
class. See ya!”, another one said and they rushed off. “Next class? The next
class starts in half an hour… and those wand movements looked a bit familiar. Could
it be…?”_

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

![Shift cipher illustration](shift_cipher.svg)

The image shows an example where the secret shift is -3. The text `wave right`,
when shifted three times backwards in the alphabet, becomes `txsb ofdeq`. That's it!
So it's not a very strong form of encryption, but it's a start.

With your newfound knowledge you should be well prepared to try and solve the
third crypto task!
