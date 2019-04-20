#!/usr/bin/env python3

import random
#from signal import alarm

OWLS ="""     ___      ,_,        ___
    (o,o)    (o,o)   ,,,(o,o),,,
    {`"'}    {`"'}    ';:`-':;'
    -"-"-    -"-"-      -"-"-"""

hole_chars = 'ABDOPQR46890&'
small_hole_chars = 'abdegopq#'
other_chars = 'CEFGHIJKLMNSTUVWXYZ12357!^*()_-=+]}[{\'"\\?/.>,<;:'
small_chars = 'cfhijklmnrstuvwxyz'

def gen_random_char(hole=False):
    if hole:
        return random.choice(hole_chars+small_hole_chars)
        #return random.choice(hole_chars)
    else:
        return random.choice(other_chars+small_chars)
        #return random.choice(other_chars)

def main():
    try:
        with open('ascii_flag.txt', 'r') as f:
            content = f.read()
    except:
        print("Error! Please contact the TG:Hack crew")
        exit()

    new_content = ''
    for c in content:
        if c == '\n':
            new_content += c
        elif c == '0':
            new_content += gen_random_char(hole=True)
        else:
            new_content += gen_random_char()
    print("{}\nHere you go! Have some fresh ASCII text:\n\n{}".format(OWLS, new_content))


if __name__ == "__main__":
    # time out after 20 seconds just in case
    #alarm(20)
    main()
    #except Exception as e:
    #    print(e)
    #    pass

