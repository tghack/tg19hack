#!/bin/bash
docker build -t kvm .
docker run -it --rm --device=/dev/kvm -p5432:5432 kvm
