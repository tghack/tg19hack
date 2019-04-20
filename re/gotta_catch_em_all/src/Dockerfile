FROM ubuntu:bionic

RUN apt update && apt install -y \
    make \
    git \
    gcc \
    byacc \
    flex \
    pkg-config \
    libpng-dev

RUN git clone https://github.com/rednex/rgbds /opt/rgbds

WORKDIR /opt/rgbds
RUN make install
RUN git clone https://github.com/pret/pokered.git /opt/pokered

WORKDIR /opt/pokered
RUN make red

ENTRYPOINT [ "/bin/bash" ]
