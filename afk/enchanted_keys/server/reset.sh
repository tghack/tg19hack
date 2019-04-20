#!/bin/bash
useradd -m -s /bin/bash tghack
chown -R root:root /home/tghack
chage -m 99999 tghack
grep -qxF 'shopt -u -o history' /home/tghack/.profile || echo 'shopt -u -o history' >> /home/tghack/.profile
mv /root/files/* /home/tghack

chmod 751 /home/pi

mkdir -p /lib/rary_/of_/secret_/flags_/
mv /root/flag.txt /lib/rary_/of_/secret_/flags_/flag.txt
chmod 444 /lib/rary_/of_/secret_/flags_/flag.txt

chmod 1770 /tmp
