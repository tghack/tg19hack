# Plastic Flagtastic Writeup
**Points: 100**

**Author: Zup**

**Difficulty: challenging**

**Category: forensics**

---

The image we got is a PNG image of some kind of modern office building. 
Let's check it using the `ls` and `file` command:

```bash
-rw-rw-r--. 1 zup zup  20M Feb 28 01:03 office.png
```

```bash
$ file office.png 
office.png: PNG image data, 5038 x 3208, 8-bit/color RGB, non-interlaced
```

This is a pretty large image, I wonder if there is anything hidden inside of it?

## Part 1: Stego

There are a few steganography tools for PNG images, e.g. 

- [Stego-toolkit](https://github.com/DominicBreuker/stego-toolkit)'s pngcheck
- [Zsteg](https://github.com/zed-0xff/zsteg)
- [Openstego](https://github.com/syvaidya/openstego)
- [Stegano](https://github.com/cedricbonhomme/Stegano)
- [Cloakedpixel](https://github.com/livz/cloacked-pixel)
- [LSBSteg](https://github.com/RobinDavid/LSB-Steganography)

We can use Zsteg to check if it finds any hidden data in the image:

```bash
$ zsteg office.png 
imagedata           .. text: ["\n" repeated 9 times]
b3,r,lsb,xy         .. text: "! $N)#rF"
b3,rgb,msb,xy       .. file: PGP\011Secret Sub-key -
b4,r,lsb,xy         .. text: "vfFTTHgUfxwwwg"
```

There does not seem to be any suspicious data in there at first glance. 
The _PGP_ data it found looks like a false positive, since it found it 
using the _most significant bytes_. Usually in PNG stegonography, you hide 
data in the _least significant bytes_ so that the image won't look much 
different from the original.

Zsteg also has an `-a` flag we can try. The `-a` flag makes Zsteg try all 
known methods. 

```bash
$ zsteg office.png -a
imagedata           .. text: ["\n" repeated 9 times]
b3,r,lsb,xy         .. text: "! $N9#rF"
b3,rgb,msb,xy       .. file: PGP\011Secret Sub-key -
b4,r,lsb,xy         .. text: "vfFTTHgUfywvwg"
b6,g,msb,xy         .. text: "4EQ$IQ4E"
b8,r,lsb,xy         .. text: "wxxwwyyzyy|}{{xywwuwvwuvyzvwxywvwwyxxxwxxywxwuvyxwvwwtwxxxxvxyxywxyyxywyxvxyxyxwwxwyxxxx{{{{{|{z|z{wwwwwxxxyxyxxxxxwvwxwwwwwwxz{yxz{{{y{yz{z{{{{|{{{{{z{{{{xwvyvxvxxvvvwwwvxxvvwwwxvy{x|wxyyyxz}wwyx{|{yuw{zyxwwxwwvvvtvututtxvwuuvvwywwwvwwvwzywvwwxwxvtuwvuvww"
b8,b,msb,xy         .. text: "uuuuuuu\ru"
b1,r,lsb,xy,prime   .. text: "oJw{2uS|2%\\~_=|z"
b1,rgb,lsb,xy,prime .. text: "297980:SnVzdCBsZWFybmVkIGFib3V0IHRoaXMgbmV3IHRlcm0gY2FsbGVkIHN0ZXJlb2xpdGhvZ3JhcGh5Li4gUHJldHR5IGNvb2wgY29uY2VwdCF0EQAAAACAPzIxjaTKyVMl5Xu6J74fq0L6fhrBJnG5J3qwqkLVIhnBYFG+J74fq0K2wyPBAAAAAIA/MjGNpMrJUyUMQMEn2JiqQjVCLMGpzrEnTmKpQvYoCsFDbMEnTmKpQjTpL8EAAAAAg"
b2,g,msb,xy,prime   .. text: "&vDfQsw~g"
b3,b,lsb,xy,prime   .. text: "aXrC(uR$"
b4,r,lsb,xy,prime   .. text: "giifWiwwfhyFtfx"
b4,g,lsb,xy,prime   .. text: "5U$ERUdETEH"
b4,b,lsb,xy,prime   .. text: "B#BtDETFHeEy"
b5,b,msb,xy,prime   .. text: "1L0 D2B8"
b8,r,lsb,xy,prime   .. text: "xwyz}{wwvyvxyxytvyyyvwy{zwwyyx{{zz{{vxwvv{}w|yvwvyvyvvuwvywwwwvvvxwytvwtvvwxxwvwxyvwuuvxvwyywywvvwxwyyyyvvy{{{x{xyy{{{zzz{y{{z}zzzzzz~"
b1,b,msb,yx         .. text: "Y}}rfM/\t"
b3,b,lsb,yx         .. text: "mt2MkJ[["
...
...
(trunkated)
```

The data found at `b1,rgb,lsb,xy,prime` seems rather suspicious.

What does this string mean?

- b1: Number of bits is 1
- rgb: The red, green and blue channel
- lsb: The least significant bit comes first
- xy: The pixel iteration order is left to right
- prime: Analyze only prime bytes/pixels

First there is a number, `297980`, followed by something that looks like a 
base64 string. The number is probably the length of the data. This is the 
same format _Stegano_ uses to hide data in images. Now we need to get the 
data out of the image. We can use Zsteg to do this by using a larger limit 
of bytes checked. (The default limit in Zsteg is 256 bytes).

```bash
$ zsteg office.png b1,rgb,lsb,xy,prime -l 1000000
```

That's a lot of data.. Let's copy the base64 data to a file:

```bash
$ zsteg office.png b1,rgb,lsb,xy,prime -l 1000000 | cut -d':' -f3 | tr -d '"\n' > b64data
```

We first cut out the part that is the base64 encoded text and then we remove 
quotes and newlines.

How many bytes are in this file now?

```bash
$ wc b64data
     0      1 297982 b64data
```

It looks like there are 297982 bytes of data, but that is 2 bytes more than 
the number we found earlier(!?).

What if we just base64 decode this data?

```bash
$ base64 -d b64data > strange_file
base64: invalid input
```

We got an error, but it looks like it managed to base64 decode the file anyway. 
There is probably some garbage at the end of the file, so just to be safe, lets 
remove it.

The last four bytes of the `b64data` file looks like this: `A=J3`. 
We know that base64 can end in `=` signs (for padding) so lets just remove the 
last two characters after the `=` sign. 

```bash
$ truncate -s-2 b64data
$ wc b64data
     0      1 297980 b64data
```

```bash
$ base64 -d b64data > strange_file
```

Nice, no errors!

---


## Part 2: Looking at the strange embedded file

What kind of file is this? We can try to check it using the `file` command.

```bash
$ file strange_file 
strange_file: data
```

This does not help us at all!

Let's look at the file in a text editor. It looks like a bunch of binary data, 
but notice the ascii text at the very top:

```
Just learned about this new term called stereolithography.. Pretty cool concept!
```

What does this mean? Stereolithography is a word that must be explored further...

Wikipedia says that [Stereolithography](https://en.wikipedia.org/wiki/Stereolithography) 
is a form of 3D printing technology patented in the 1980s. 

If we take a closer look at the picture again, and use reverse image search on 
Google, we find out that this is the first 3D printed office built in Dubai in 2016. 

Both the strange text we found and the image indicates that this file is some 
sort of file for 3D printers.

3D printer software uses all sort of files:

- .stl (binary)
- .stl (ascii)
- .obj
- .gcode
- .vrml
- .amf
- .x3d

And many more.

Since our file looked like a binary file, let's take a look at the STL format. 
The .STL file type is also an abbreviation for _Stereolithograpy_.
[Wikipedia](https://en.wikipedia.org/wiki/STL_(file_format)#Binary_STL) says that 
a binary STL file starts with an 80 bytes long header. There are 80 characters in 
the strange text we found as well. Coincidence? I think not :)

Alright, now we just got to find a program that can open an STL file to show us 
what kind of 3D model this is. We can use:

Desktop programs:

* Ultimaker CURA
* FreeCAD
* Blender
* Slic3r

Web apps (Easier for viewing STL files without downloading any program):

* <https://openjscad.org/>
* <https://3dviewer.net/>
* <https://www.viewstl.com/> 
* <https://www.blockscad3d.com/editor/>

For a list of more useful 3D printer software check out 
<https://reprap.org/wiki/Useful_Software_Packages>


We first rename our STL file to `strange_file.stl` and open it in FreeCAD. 
After rotating the figure we can see that it's a 3D figure of a flag!

![Flag](flag.png)

**Flag**: `TG19{3D_printing_started_in_the_80s}`
