FROM ubuntu:bionic

RUN apt update && apt full-upgrade -y && apt install -y xinetd
RUN useradd -m -s /bin/bash tghack

COPY flip /home/tghack/flip
RUN chmod 755 /home/tghack/flip

COPY flip.xinetd /etc/xinetd.d/flip
RUN chmod 644 /etc/xinetd.d/flip

COPY flag.txt /home/tghack/flag.txt
RUN chmod 444 /home/tghack/flag.txt

COPY wrap.sh /opt/wrap.sh
RUN chmod 755 /opt/wrap.sh

RUN chmod 1770 /tmp
RUN chown -R root:root /home/tghack

CMD service xinetd start && /bin/bash
