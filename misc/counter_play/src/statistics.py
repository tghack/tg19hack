#!/usr/bin/env python
from pwn import *

LOCAL = False

chmap = {}

for x in range(300):
    line = 0
    if LOCAL:
        r = remote('localhost', 2018)
    else:
        r = remote('counter.tghack.no', 2018)
    _ = r.recvuntil("text:\n\n")
    data = r.recvall()
    
    pos = 0
    for ch in data:
        if ch == '\n':
            line += 1
            pos = 0
            continue
        if line not in chmap:
            chmap[line] = {}
        if pos not in chmap[line]:
            chmap[line][pos] = {}
        if ch not in chmap[line][pos]:
            chmap[line][pos][ch] = 1
        
        chmap[line][pos][ch] += 1
        
        pos += 1
    
    log.info(data)
    r.close()
 
with open('statistics.txt', 'a') as f:
    for line in chmap:
        for pos in chmap[line]:
            v = []
            for ch in chmap[line][pos]:
                v.append("%s" % (ch))
            log.info("Line[%s] Pos[%s]: %s" % (line+1, pos+1, ' '.join(v)))
            f.write(("Line[%s] Pos[%s]: %s\n" % (line+1, pos+1, ' '.join(v))))
