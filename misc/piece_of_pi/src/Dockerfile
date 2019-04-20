FROM ubuntu:bionic

RUN sed -Ei 's/^# deb-src /deb-src /' /etc/apt/sources.list
RUN apt update && apt-get build-dep -y qemu-system-arm && apt install -y vim git
COPY ./vm /opt/
WORKDIR /opt/
RUN apt install -y ca-certificates

ENTRYPOINT [ "./build.sh" ]
