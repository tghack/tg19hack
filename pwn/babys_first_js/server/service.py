#!/usr/bin/env python3
import subprocess
import os
import sys


template = """
code = `
{}
`

Realm.create();
Realm.eval(1, code);
"""

def main():
    temp = open("/tmp/foobar.js", "w+")
    print("send me some JS, stop with EOF")
    data = ""
    while True:
        tmp = input("")
        print("line read: {}".format(tmp))
        sys.stdout.flush()
        if tmp.startswith("EOF"):
            print("Done reading, executing JS!")
            break
        data += tmp + "\n"
    temp.write(template.format(data + "\n"))
    temp.close()

    sys.stdout.flush()

    proc = subprocess.Popen(["/home/tghack/d8", temp.name])
    proc.wait()
    os.unlink(temp.name)

if __name__ == "__main__":
    main()
