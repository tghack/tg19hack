FROM ubuntu:xenial

RUN dpkg --add-architecture i386 && apt update && apt full-upgrade -y && apt install -y xinetd libc6:i386
RUN useradd -m -s /bin/bash tghack

COPY pwntion3 /home/tghack/pwntion3
RUN chmod 765 /home/tghack/pwntion3

COPY banner.txt /home/tghack
RUN chmod 644 /home/tghack/banner.txt

COPY flag.txt /home/tghack
RUN chmod 644 /home/tghack/flag.txt

COPY pwntion3.xinetd /etc/xinetd.d/pwntion3
RUN chmod 644 /etc/xinetd.d/pwntion3

COPY wrap.sh /opt/wrap.sh
RUN chmod 755 /opt/wrap.sh

RUN chmod 1770 /tmp
RUN chown -R root:root /home/tghack

CMD service xinetd start && /bin/bash
