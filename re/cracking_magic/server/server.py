#!/usr/bin/env python3
from subprocess import run, PIPE
import sys


def read_flag():
    return open("/home/tghack/flag.txt").read()


def check_serial(s):
    proc = run(["/home/tghack/key_check.elf"], input=(s + "\n").encode("utf-8"), stdout=PIPE)
    return not proc.returncode


def main():
    serials = []
    for i in range(250):
        s = input("serial {}/{}: ".format(i + 1, 250))
        if not check_serial(s):
            print("Wrong! Try again")
            sys.exit()
        if s in serials:
            print("You already used that serial!")
            sys.exit()

        serials.append(s)
        if i != 249:
            print("Ok, next!")

    print("Thank you so much!")
    flag = read_flag()
    print("Here's the flag: {}".format(flag))


if __name__ == "__main__":
    main()
