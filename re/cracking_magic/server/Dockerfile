FROM ubuntu:bionic

RUN apt update && apt install -y socat python3
RUN useradd -m tghack
COPY run.sh /home/tghack
COPY server.py /home/tghack
COPY key_check.elf /home/tghack
COPY flag.txt /home/tghack

ENTRYPOINT [ "/home/tghack/run.sh" ]
