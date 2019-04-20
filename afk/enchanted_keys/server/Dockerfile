FROM ubuntu:bionic

RUN apt update && apt full-upgrade -y
RUN useradd -m -s /bin/bash tghack
RUN chage -m 99999 tghack
RUN echo 'shopt -u -o history' >> /home/tghack/.profile

COPY files /home/tghack

COPY flag.txt /lib/rary_/of_/secret_/flags_/flag.txt
RUN chmod 444 /lib/rary_/of_/secret_/flags_/flag.txt

RUN chmod 1770 /tmp
RUN chown -R root:root /home/tghack

USER tghack
WORKDIR /home/tghack

CMD /bin/bash

