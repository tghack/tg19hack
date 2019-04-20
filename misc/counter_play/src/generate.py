#!/usr/bin/env python3

import random

hole_chars = 'ABDOPQR46890&'
small_hole_chars = 'abdegopq'
other_chars = 'CEFGHIJKLMNSTUVWXYZ12357!^*()_-=+]}[{\'"\\?/.>,<;:'
small_chars = 'cfhijklmnrstuvwxyz'

def gen_random_char(hole=False):
    if hole:
        return random.choice(hole_chars+small_hole_chars)
        #return random.choice(hole_chars)
    else:
        return random.choice(other_chars+small_chars)
        #return random.choice(other_chars)

with open('ascii_flag.txt', 'r') as f:
    content = f.read()

new_content = ''
for c in content:
    if c == '\n':
        new_content += c
    elif c == '0':
        new_content += gen_random_char(hole=True)
    else:
        new_content += gen_random_char()

with open('flag.enc', 'w') as f:
    f.write(new_content)
