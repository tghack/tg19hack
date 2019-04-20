# Writeup for filemagic

## Task description
**Points: 70**

**Difficulty: easy**

**Category: forensic**

--


## Writeup
 
First we start by inspecting the given file. We can for starters use the command
`file` as an indication on what type of file this is:
```bash
$ file store.bin 
store.bin: DOS/MBR boot sector, code offset 0x3c+2, OEM-ID "mkfs.fat", sectors/cluster 4, root entries 512, sectors 2048 (volumes <=32 MB), Media descriptor 0xf8, sectors/FAT 2, sectors/track 32, heads 64, serial number 0x71a6dccf, label: "magic      ", FAT (12 bit)
``` 


`file` has identified the file for us as a "FAT (12bit) filesystem". Cool, lets
attempt to mount it so we easier can look at the content of the filesystem:


```bash
(optional) $ sudo mkdir /mnt/loopmount
$ sudo mount -o loop store.bin /mnt/loopmount
```
(Or choose another mount location if you desire.)

All we need is to set the loop option and mount selects the right filesystem
type. Now we can list out the contents of the mounted path and observe the
content:

```bash
$ ls /mnt/loopmount 
treasures

$ ls /mnt/loopmount/treasures/             
doughloaf.png
```

Seems like a picture based on the file extension, but lets double check:

```bash
$ file /mnt/loopmount/treasures/doughloaf.png 
/mnt/loopmount/treasures/doughloaf.png: PNG image data, 550 x 550, 8-bit/color RGBA, non-interlaced
``` 

And when we display the photo, we see the flag :)

Just remember to unmount the filesystem before moving on to the next task:

```
sudo umount /mnt/loopmount
```



... But that's not the only way to solve this task!
Forensic tools like `foremost` or `binwalk` can sometimes carve out the file for
us like this:

```bash
$ foremost store.bin
```

You will then find the picture in the out output folder.

Binwalk also works if you extract _all_ filetypes:

```
$ binwalk --dd='.*' store.bin
```

You can find the image in the "_store.bin.extracted" folder.

GG.
