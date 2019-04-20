FROM ubuntu:bionic

RUN apt update && apt install -y socat python-minimal
RUN useradd -m tghack
COPY qemu-system-arm /home/tghack/
COPY run.py /home/tghack
COPY start_server.sh /home/tghack

# just to have all the libs...
RUN apt install -y qemu-system-arm

ENTRYPOINT [ "/home/tghack/start_server.sh" ]
