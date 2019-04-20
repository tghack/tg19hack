dd if=/dev/zero of=store.bin bs=1M count=1
mkfs.vfat store.bin -n "magic"
sudo mount -o loop store.bin /mnt/loopmount
sudo mkdir /mnt/loopmount/treasures
sudo cp doughloaf.png /mnt/loopmount/treasures/
sudo umount /mnt/loopmount
