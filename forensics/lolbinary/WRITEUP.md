# Writeup for [lolbinary](README.md)

## Task description
**Points 350**

**Difficulty: Hard**

**Category: forensics**

**Sub-Category: reverse engineering**

--

 
## Writeup
  
In this task we got a hint that we are looking for an interesting binary in the network stream.
There are multiple binary formats that could have been used, but the first that comes to mind are PE executables and ELF executables.

To find packets that might contain these files, we can use the powerful wireshark display filter: `frame ~ "cannot be run"`.
If we now follow this tcpdstream we see that this is a PE executable file. We then save this raw tcp stream to file to analyse it in tools more suited for PE files.

This binary only contains junk code and only ends up printing `lol` after wasting our time doing random stuff, quite literally.
But when we look at this file in a hex viewer or in a tool like `resource hacker` we see some base64 data hidden in the resoruce part of the PE file.

When we open resource hacker and pull the PE executable file into it, we see that it contains RCData called `olo` that contains base64data. The base64 string "TV" is equal to "MZ" decoded which is the magic header for windows PE executables. This means that we have another payload to analyse, so lets grab the base64 data in resource hacker by right clicking on `olo` and saving it as a binary.
Then decode the base64 data and save the decoded content as `lol_payload.exe`.

If we look closly at the new binary in a hex editor, we see that it only contains two sections, `lol0` and `lol1`:

```
000001e0  00 00 00 00 00 00 00 00  4c 4f 4c 30 00 00 00 00  |........LOL0....|
000001f0  00 80 00 00 00 10 00 00  00 00 00 00 00 04 00 00  |................|
00000200  00 00 00 00 00 00 00 00  00 00 00 00 80 00 00 e0  |................|
00000210  4c 4f 4c 31 00 00 00 00  00 20 00 00 00 90 00 00  |LOL1..... ......|
00000220  00 20 00 00 00 04 00 00  00 00 00 00 00 00 00 00  |. ..............|
00000230  00 00 00 00 40 00 00 e0  2e 72 73 72 63 00 00 00  |....@....rsrc...|
00000240  00 10 00 00 00 b0 00 00  00 06 00 00 00 24 00 00  |.............$..|
00000250  00 00 00 00 00 00 00 00  00 00 00 00 40 00 00 c0  |............@...|
00000260  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  |................|
*
000003d0  00 00 00 00 00 00 00 00  00 00 00 33 2e 39 34 00  |...........3.94.|
000003e0  55 50 58 21 0d 09 02 08  9b 2a df fb 2c 44 43 44  |UPX!.....*..,DCD|
000003f0  ee 89 00 00 61 1c 00 00  00 44 00 00 26 02 00 34  |....a....D..&..4|
```


This is strange and might indicate that this binary is packed as we expected more and different sections in a normal PE file.
A but further down we see the string `UPX` that conclides with the two sections that this binary is packed, most likely with `UPX`.
However, we cannot directly unpack this binary with upx as it expects `UPX0` and `UPX1` resources. By changing this in the header, we are finally able to unpack this executable:

```
$ upx -d packedpayload.exe
                       Ultimate Packer for eXecutables
                          Copyright (C) 1996 - 2018
UPX 3.95        Markus Oberhumer, Laszlo Molnar & John Reiser   Aug 26th 2018

        File size         Ratio      Format      Name
   --------------------   ------   -----------   -----------
     17408 <-     10752   61.76%    win32/pe     packedpayload.exe

Unpacked 1 file. 
```

Now the real magic begins.

Looking at disassembled code, strings and decompiled code of this binary, we see some debug info left that indicates a possible http request, but we see no http headers in the strings. This might be because of encryption/encoding of the strings to make reversing this sample harder. By looking for encryption/decryption functions or by debugging, we find usage of the decrypt function:

(from ghidra decompiler view)
```
  FUN_00401010(local_44,"meemfo$ieg");
  local_8 = 0;
  FUN_00401010(local_2c,".");
  local_8._0_1_ = 1;
```
Here we see that `meemfo$ieg` is send as the second parameter and the first parameter might be where the decrypted string is stored.
Looking into FUN_00401010 in ghidras decompiler:

```c
  pcVar5 = param_2 + 1;
  pcVar6 = param_2;
  do {
    cVar1 = *pcVar6;
    pcVar6 = pcVar6 + 1;
  } while (cVar1 != 0);
  pcVar6 = pcVar6 + -(int)pcVar5;
  iVar7 = 0;
  local_1c = param_1;
  if (0 < (int)pcVar6) {
    do {
      uVar2 = param_1[4];
      bVar4 = param_2[iVar7] ^ (byte)pcVar6;
      pcVar5 = (char *)((uint)pcVar5 & 0xffffff00 | (uint)bVar4);
      if (uVar2 < (uint)param_1[5]) {
        param_1[4] = uVar2 + 1;
        puVar3 = param_1;
        if (0xf < (uint)param_1[5]) {
          puVar3 = (undefined4 *)*param_1;
        }
        *(byte *)((int)puVar3 + uVar2) = bVar4;
        *(undefined *)((int)puVar3 + uVar2 + 1) = 0;
      }
      else {
        local_1c = (undefined4 *)((uint)local_1c & 0xffffff00);
        FUN_00401e40(param_1,pcVar5,local_1c,bVar4);
        pcVar5 = extraout_ECX;
      }
      iVar7 = iVar7 + 1;
    } while (iVar7 < (int)pcVar6);
  }
  *in_FS_OFFSET = local_10;
  return param_1;
```

This is a simple xor key encrypton/decryption function that uses the length of a string as the key to xor with. Note that this is the length of the hex-decoded string that is used.

In pseudocode it looks something like this:

```c
for(int i=0;i<length(string);i++) {
    string[i] ^ length(string)
}
```


Now if we decrypt all strings that get passed into the decrypt function, we find all the parts of the http get request, as well as `google.com`, `/`, `notc2.tghack.no` and `/get_flag`.
The binary by default sends a http get request to "google/" using a special user-agent `secretstringkey`, but the other url and domain is not currently in use.

If we attempt to make a get request using the known useragent `secretstringkey` to "notc2.tghack.no" with url "/get_flag" we get a hex value in return:

```
4b582e26646c6a7c77407e406d7a6c706a6d7c7a796a73407d76717e6d6662
```

If we decode this from hex and use the same encryption routine with xor of the length of the string we should get the flag.
I wrote a python3 script to make the get request and decode the result:

```python
#!/usr/bin/env python3
import requests
import binascii

url="http://notc2.tghack.no/get_flag"
headers = {
    'User-Agent': 'secretstringkey'
}

data = requests.get(url, headers=headers)
flagenc=data.text.strip()
lol=binascii.unhexlify(flagenc)
key=len(lol)
flag=""

for c in lol:
    flag+=chr(c ^ key)

print(flag)
```
Running this prints the flag:

TG19{such_a_resourceful_binary}
