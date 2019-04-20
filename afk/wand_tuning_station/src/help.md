What to do when there is something wrong with the PI?

We took a backup of the SD card, so in worst case it's possible to overwrite it with our backup.
The backup is located at: zup's computer atm :PPP

```
sudo dd bs=4M if=~/wand_tuning_station.img of=/dev/mmcblk0

```

The bs=4M option sets the 'block size' on the SD card to 4Meg.  If you get any warnings, then change this to 1M instead, but that will take a little longer to write.

Again, wait while it completes.  Before ejecting the SD card, make sure that your Linux PC has completed writing to it using the command:

```
sudo sync
```
