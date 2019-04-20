#!/usr/bin/env python3

with open('header.txt') as f:
    header = f.readline().strip()
    if len(header) > 80:
        raise ValueError
    repr(header)

header = header.ljust(80)

with open('base.stl', 'rb') as f:
    data = f.read()

with open('flag.stl', 'wb') as f:
    f.seek(0)
    if len(header) != 80:
        raise ValueError
    f.write(header.encode('ascii')+data[80:])
