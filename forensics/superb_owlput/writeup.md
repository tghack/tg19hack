# Writeup for Superb Owlput 

## Task description
**Points: 150**

**Author: bolzzy**

**Difficulty: challenging**

**Category: forensic**



## Writeup

Right off the bat we are given a PCAP file that contains some strange traffic.
When we inspect this in a packet analyzer like tcpdump/tshark/wireshark we can see a lot of DNS A record requests from one client as well as some TCP traffic going on:

```
tcpdump -nnr superb-owlput.pcap
reading from file superb-owlput.pcap, link-type EN10MB (Ethernet)
04:40:00.242979 IP 172.19.1.50.51016 > 172.19.0.3.53: 43985+ A? ffd8ffe000104a46494600010101004800480000ffe100a24578696600004d.dw.tghekk.local. (96)
04:40:00.605741 IP 172.19.0.3.53 > 172.19.1.50.51016: 43985- 1/0/0 A 0.0.0.0 (190)
04:40:00.924734 IP 172.19.1.50.56478 > 172.19.0.3.53: 5099+ A? 4d002a000000080005011a0005000000010000004a011b0005000000010000.dw.tghekk.local. (96)
04:40:01.160833 IP 172.19.0.3.53 > 172.19.1.50.56478: 5099- 1/0/0 A 0.0.0.0 (190)
04:40:01.350557 IP 172.19.1.50.61903 > 172.19.0.3.53: 25357+ A? 0052012800030000000100020000013b00020000003f0000005a0213000300.dw.tghekk.local. (96)
04:40:01.823901 IP 172.19.0.3.53 > 172.19.1.50.61903: 25357- 1/0/0 A 0.0.0.0 (190)
04:40:01.975301 IP 172.19.1.50.56812 > 172.19.0.3.53: 21712+ A? 00000100010000000000000000004800000001000000480000000156456378.dw.tghekk.local. (96)
04:40:02.099830 IP 172.19.0.3.53 > 172.19.1.50.56812: 21712- 1/0/0 A 0.0.0.0 (190)
04:40:02.392485 IP 172.19.1.50.45705 > 172.19.0.3.53: 63098+ A? 4f587455534556665630464d54464e6651564a4658304e50566b5653525552.dw.tghekk.local. (96)
04:40:02.617591 IP 172.19.0.3.53 > 172.19.1.50.45705: 63098- 1/0/0 A 0.0.0.0 (190)
04:40:02.653258 IP 172.19.1.50.62865 > 172.19.0.3.53: 19458+ A? 6656306c555346394e5155644a5130464d58314e425446523943670000ffdb.dw.tghekk.local. (96)
04:40:02.978118 IP 172.19.0.3.53 > 172.19.1.50.62865: 19458- 1/0/0 A 0.0.0.0 (190)
04:40:03.084983 IP 172.19.1.50.56690 > 172.19.0.3.53: 18863+ A? 0043000c08090b09080c0b0a0b0e0d0c0e121e1412111112251b1c161e2c27.dw.tghekk.local. (96)
04:40:03.228086 IP 172.19.0.3.53 > 172.19.1.50.56690: 18863- 1/0/0 A 0.0.0.0 (190)
04:40:03.475790 IP 172.19.1.50.40291 > 150.4.171.134.13436: Flags [.], seq 3981215220:3981215262, ack 0, win 65000, length 42
04:40:03.561734 IP 150.4.171.134.13436 > 172.19.1.50.40291: Flags [.], seq 1026886554:1026887214, ack 42, win 65000, length 660

```

In this example I'm using tcpdump as the first indication of the contents of this packet capture, but as the PCAP is 5MB in size and contains a lot of packets, I switch to Wireshark to gain a better overview using the "Statistics > Protocol Hierarchy" from the menu bar.

We see that over 93% of all packets in this capture is actually just DNS requests and responses, which is quite a lot of DNS traffic.
When we go further into the statistics by selecting "Statistics > Conversations", we see that almost all DNS requests are sent by IP 172.19.1.50. This does not look good. 
There are also some TCP traffic going on, but as we have strong indications that some kind of `DNS tunneling` is going on, we can ignore those for now.

Looking at the DNS requests, we see that the suspicious requests are A record requests of "something" .dw.tghekk.local and the response is "0.0.0.0" which is actually a non-valid IPv4 "meta-address".

```
    1   0.000000  172.19.1.50 51016 172.19.0.3   53 DNS 138 Standard query 0xabd1 A ffd8ffe000104a46494600010101004800480000ffe100a24578696600004d.dw.tghekk.local
    2   0.362762   172.19.0.3 53 172.19.1.50  51016 DNS 232 Standard query response 0xabd1 A ffd8ffe000104a46494600010101004800480000ffe100a24578696600004d.dw.tghekk.local A 0.0.0.0
    3   0.681755  172.19.1.50 56478 172.19.0.3   53 DNS 138 Standard query 0x13eb A 4d002a000000080005011a0005000000010000004a011b0005000000010000.dw.tghekk.local
    4   0.917854   172.19.0.3 53 172.19.1.50  56478 DNS 232 Standard query response 0x13eb A 4d002a000000080005011a0005000000010000004a011b0005000000010000.dw.tghekk.local A 0.0.0.0
    5   1.107578  172.19.1.50 61903 172.19.0.3   53 DNS 138 Standard query 0x630d A 0052012800030000000100020000013b00020000003f0000005a0213000300.dw.tghekk.local
    6   1.580922   172.19.0.3 53 172.19.1.50  61903 DNS 232 Standard query response 0x630d A 0052012800030000000100020000013b00020000003f0000005a0213000300.dw.tghekk.local A 0.0.0.0
    7   1.732322  172.19.1.50 56812 172.19.0.3   53 DNS 138 Standard query 0x54d0 A 00000100010000000000000000004800000001000000480000000156456378.dw.tghekk.local
    8   1.856851   172.19.0.3 53 172.19.1.50  56812 DNS 232 Standard query response 0x54d0 A 00000100010000000000000000004800000001000000480000000156456378.dw.tghekk.local A 0.0.0.0
    9   2.149506  172.19.1.50 45705 172.19.0.3   53 DNS 138 Standard query 0xf67a A 4f587455534556665630464d54464e6651564a4658304e50566b5653525552.dw.tghekk.local
   10   2.374612   172.19.0.3 53 172.19.1.50  45705 DNS 232 Standard query response 0xf67a A 4f587455534556665630464d54464e6651564a4658304e50566b5653525552.dw.tghekk.local A 0.0.0.0
```

As this is a DNS A record and the response is not containing any extra data, this means that all transferred data must be in the request hostname itself.
Also we observe that ".dw.tghekk.local" is in every record, and "dw" can i.e. mean something like "DoWnload". The top level domain is "local" and not a real TLD, but can be used locally. This is however not important in solving this task. But what is important is the sub sub domain that seems to be random characters from '0' to '9' and 'a' to 'f'. If we try to decrypt the first sub sub domain as a hex string, we can actually see that this might look like a JPEG header based on the "JFIF" content! 

```
Python 3.7.3
>>> import codecs
>>> print(codecs.decode("ffd8ffe000104a46494600010101004800480000ffe100a24578696600004d","hex"))
b'\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01\x01\x01\x00H\x00H\x00\x00\xff\xe1\x00\xa2Exif\x00\x00M'
```

To automate the decoding of the sub sub domains, I wrote a scapy script:

```
from scapy.all import *
import binascii

pkts = rdpcap("superb-owlput.pcap")

out=""

for p in pkts:
    if p.dport==53:
        if "dw" in p[DNSQR].qname.decode("utf-8"):
            x = p[DNSQR].qname.decode("utf-8").split(".")[0]
            out+=x

with open("outfile","wb") as f:
    f.write(binascii.unhexlify(out))
```

When running this script and looking at the "outfile", we see that this is really a JPEG Picture that can be displayed without any errors.
But the picture does not display the flag itself, so lets look at the pictures metadata using the unix tool `exiftool`


```
exiftool outfile
ExifTool Version Number         : 11.30
File Name                       : outfile
Directory                       : .
File Size                       : 402 kB
File Modification Date/Time     : 2019:04:01 23:17:23+02:00
File Access Date/Time           : 2019:04:01 23:17:37+02:00
File Inode Change Date/Time     : 2019:04:01 23:17:23+02:00
File Permissions                : rw-r--r--
File Type                       : JPEG
File Type Extension             : jpg
MIME Type                       : image/jpeg
JFIF Version                    : 1.01
Exif Byte Order                 : Big-endian (Motorola, MM)
X Resolution                    : 72
Y Resolution                    : 72
Resolution Unit                 : inches
Artist                          : VEcxOXtUSEVfV0FMTFNfQVJFX0NPVkVSRURfV0lUSF9NQUdJQ0FMX1NBTFR9Cg
Y Cb Cr Positioning             : Centered
Image Width                     : 2380
Image Height                    : 3397
Encoding Process                : Baseline DCT, Huffman coding
Bits Per Sample                 : 8
Color Components                : 3
Y Cb Cr Sub Sampling            : YCbCr4:2:0 (2 2)
Image Size                      : 2380x3397
Megapixels                      : 8.1
```

That artist name sure is way too weird looking and matches a base64 encoded string, let's decrypt it:

```
echo "VEcxOXtUSEVfV0FMTFNfQVJFX0NPVkVSRURfV0lUSF9NQUdJQ0FMX1NBTFR9Cg" | base64 -d
TG19{THE_WALLS_ARE_COVERED_WITH_MAGICAL_SALT}
base64: invalid input
```
We ignore the error and enjoy our flag :)
