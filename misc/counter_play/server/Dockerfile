FROM ubuntu:bionic

RUN apt update && apt full-upgrade -y && apt install -y xinetd python3
RUN useradd -m -s /bin/bash tghack

COPY server.py /home/tghack/counterplay.py
RUN chmod 755 /home/tghack/counterplay.py

COPY counterplay.xinetd /etc/xinetd.d/counterplay
RUN chmod 644 /etc/xinetd.d/counterplay

COPY ascii_flag.txt /home/tghack/ascii_flag.txt
RUN chmod 644 /home/tghack/ascii_flag.txt

COPY wrap.sh /opt/wrap.sh
RUN chmod 755 /opt/wrap.sh

RUN chmod 1770 /tmp
RUN chown -R root:root /home/tghack

CMD service xinetd start && /bin/bash
