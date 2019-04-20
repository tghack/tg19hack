from z3 import *
from pwn import *

s = Solver()

serial = [ BitVec("{}".format(i), 32) for i in range(24) ]
for i in range(24):
    # ascii
    s.add(serial[i] >= 48)
    s.add(serial[i] <= 122)
    s.add(serial[i] != ord(":"))
    s.add(serial[i] != ord(";"))
    s.add(serial[i] != ord("<"))
    s.add(serial[i] != ord("="))
    s.add(serial[i] != ord(">"))
    s.add(serial[i] != ord("?"))
    s.add(serial[i] != ord("@"))
    s.add(serial[i] != ord("\\"))
    s.add(serial[i] != ord("["))
    s.add(serial[i] != ord("]"))
    s.add(serial[i] != ord("^"))
    s.add(serial[i] != ord("_"))
    s.add(serial[i] != ord("`"))


for i in range(0, 12, 2):
    a = serial[i]
    b = serial[i + 1]
    s.add((a ^ b ^ 0x42) < 70)

for i in range(12, 24, 2):
    a = serial[i]
    b = serial[i + 1]
    s.add((a ^ b ^ 0x13) > 30)

# https://yurichev.com/writings/SAT_SMT_by_example.pdf
# page 475
results = []
while True:
    if len(results) >= 250:
        break
    if s.check() == sat:
        m = s.model()
        #print m[serial]
        #print m
        results.append(m)

        block = []
        for d in m:
            if d.arity() > 0:
                raise Z3Exception("uninterpreted functions are not supported")
            c = d()
            if is_array(c) or c.sort().kind() == Z3_UNINTERPRETED_SORT:
                raise Z3Exception("arrays and uninterpreted sorts are not supported")
            block.append(c != m[d])
        s.add(Or(block))
    else:
        print "results: {}".format(len(results))

def bv2int(bv):
    return int(str(bv))

serials = []
for res in results:
    serials.append("".join([chr(bv2int(res[serial[i]])) for i in range(24)]))

r = remote("localhost", 2222)
for i in range(250):
    print(r.recvuntil(": "))
    r.sendline(serials[i])
    print(r.recvline())

r.interactive()
