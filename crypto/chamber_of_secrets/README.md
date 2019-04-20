# The Chamber of Secrets
**Points: 300**

**Author: Chabz**

**Difficulty: hard**

**Category: crypto**
___

I was walking down a dark corridor one evening when I 
suddenly heard some whispering from the walls around me.
I couldn't quite hear what it said, so when the thing 
whispering started moving, I obviously followed.
What could go wrong, right? After a while, I turned a corner
and looked right into some red text on a wall. It said:

```
public(h, a, b, q, g)
h = (829999038570486 : 549144410878897 : 1)
a = -3
b = 313205882961673
q = 1125899906842597
g = (1115545019992514 : 78178829836422 : 1)
c = ((700253548714057 : 421820716153583 : 1), (470712751668926 : 131989609316847 : 1))

sTokhflo9WHPQB8JHEm0OVG2SwUA/sHaP0yFv9T2kmoZjC5g46eeRM8M8CGRj8bV/NxY4VJ8Ls0=
```

When standing there pondering who in their right minds
would write something like that on a wall, the whispers
grew louder and I finally heard what it said:

```python
key =  SHA256.new()
key.update(secret)

def bf_encrypt(key, message):
    bs = Blowfish.block_size
    iv = Random.new().read(bs)
    cipher = Blowfish.new(key, Blowfish.MODE_CBC, iv)
    pad_len = bs - divmod(len(message), bs)[1]
    padding = [pad_len]*pad_len
    padding = pack('b'*pad_len, *padding)
    return base64.b64encode(iv + cipher.encrypt(message + padding))
```

All of this sounds like gibberish to me, but maybe
someone capable of speaking old, mythical languages
can decipher the whispers and recover the secrets of
old...
