#!/bin/bash

if ! test -d "qemu"; then
	git clone --depth 1 git://git.qemu-project.org/qemu.git qemu
	#git clone git://git.qemu-project.org/qemu.git qemu
fi

cd qemu
#git submodule update --depth 1 --init --recursive
git submodule update 

if ! test -d "build"; then
	mkdir build
fi

# apply patch
patch -p1 < ../piece_of_pi_qemu.patch

cd build

../configure --target-list=arm-softmmu \
			 --disable-slirp \
			 --disable-docs \
			 --disable-gnutls \
			 --disable-nettle \
			 --disable-snappy \
			 --disable-bzip2 \
			 --disable-lzo \
			 --disable-opengl \
			 --disable-gtk \
			 --disable-sdl \
			 --disable-vnc \
			 --disable-capstone
			 #--enable-curses
			 #--enable-seccomp
make -j8

cp arm-softmmu/qemu-system-arm /opt/
