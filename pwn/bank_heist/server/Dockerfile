FROM ubuntu:bionic

RUN apt update && apt full-upgrade -y && apt install -y xinetd
RUN useradd -m -s /bin/bash tghack

COPY kvm /home/tghack/kvm
RUN chmod 755 /home/tghack/kvm

COPY kvm.xinetd /etc/xinetd.d/kvm
COPY flag.txt /home/tghack/flag.txt
RUN chmod 444 /home/tghack/flag.txt

COPY wrap.sh /opt/wrap.sh
RUN chmod 755 /opt/wrap.sh

RUN chown -R root:root /home/tghack
EXPOSE 5432

CMD chmod 666 /dev/kvm && service xinetd start && /bin/bash

