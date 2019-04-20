#!/usr/bin/env python3
import binascii
import sys


def print_flag():
    enc = "1605737b39323b362a2d2c1d203b3627212d26271d2b2c1d362a271d2a2d3731273f"
    enc = binascii.unhexlify(enc)
    key = 0x42
    dec = ""
    for i in enc:
        dec += chr(i ^ key)
    print(dec)


def main(code):
    if code == 1337:
        print_flag()
    else:
        print("wrong!")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("error! missing magic code!")
        sys.exit()
    main(int(sys.argv[1]))
