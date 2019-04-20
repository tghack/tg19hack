#!/bin/bash
# Using stegano-lsb for encoding. I use the Erastothenes generator (Hide msg using sieves of erastothenes)
stegano-lsb-set hide -i 3doffice_of_the_future.jpg -f flag.stl -g eratosthenes -o ../uploads/office.png
#stegano-lsb-set hide -i 3doffice_of_the_future.jpg -f flag.x3d -g eratosthenes -o ../uploads/office2.png
