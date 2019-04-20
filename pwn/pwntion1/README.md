# Introduction to Pwntions
**Points: 50**

**Author: maritio_o**

**Difficulty: n00b/easy**

**Category: pwn**

---

_"As there is little foolish wand-waving here, many of you will hardly believe 
this is magic. I don't expect you will really understand the beauty of the 
softly simmering cauldron with its shimmering fumes, the delicate power of 
liquids that creep through the human veins, bewitching the minds, ensnaring 
the senses... I can teach you how to bottle fame, brew glory, even put a stopper
death - if you aren't as big a bunch of dunderheads as I usually have to teach."_
    
—Professor maritio\_o's introduction of the subject

As you've understood from the 
[introduction to **pwn**tions lectures](https://github.com/PewZ/tg19hack/blob/n00b-pwntion1/tutorial/pwntion/01introduction.md), 
we want to teach you the art of stack overflows. Stack overflow is an ancient way 
of making pwntions, and neither wizards or muggles have gotten affected by this 
pwntion in many decades. 

In the classes we tested our pwntions on a house elf vulnerable to this stack
overflow. Can you brew this right, and give it to him? Don't worry, it is not 
deadly.. He will just grow a large nose, and tell us his deepest secrets..

Here, take this [binary file](uploads/pwntion1_public) and the 
[source code](uploads/pwntion1_public.c) for local pwning.

```
nc pwntion1.tghack.no 1061
```

<details><summary>Tip</summary>

1. The file expects to read a file called `banner.txt`. For the binary to
work locally, you should make a file with that name and put whatever you 
would like into it. 

2. Read the Introduction to Pwntions tutorial to learn about this type of 
stack overflow problem.
</details>
