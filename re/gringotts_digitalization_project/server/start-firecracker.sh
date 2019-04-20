#!/bin/sh

DIR=`pwd`
SOCKNAME=/tmp/firecracker.socket
KERNEL_NAME=$DIR/vmlinux.elf
ROOTFS=$DIR/rootfs.ext4

curl --unix-socket $SOCKNAME -i \
    -X PUT "http://localhost/machine-config" \
    -H "accept: application/json" \
    -H "Content-Type: application/json" \
    -d "{
        \"vcpu_count\": 1,
        \"mem_size_mib\": 512
    }"

curl --unix-socket $SOCKNAME -i \
    -X PUT "http://localhost/boot-source" \
    -H "accept: application/json" \
    -H "Content-Type: application/json" \
    -d "{
        \"kernel_image_path\": \"$KERNEL_NAME\",
        \"boot_args\": \"console=ttyS0 reboot=k panic=1 pci=off root=/dev/vda\"
    }"

curl --unix-socket $SOCKNAME -i \
    -X PUT "http://localhost/drives/rootfs" \
    -H "accept: application/json" \
    -H "Content-Type: application/json" \
    -d "{
        \"drive_id\": \"rootfs\",
        \"path_on_host\": \"$ROOTFS\",
        \"is_root_device\": true,
        \"is_read_only\": false
    }"

curl --unix-socket $SOCKNAME -i \
    -X PUT "http://localhost/actions" \
    -H  "accept: application/json" \
    -H  "Content-Type: application/json" \
    -d "{
        \"action_type\": \"InstanceStart\"
     }"

rm $SOCKNAME
