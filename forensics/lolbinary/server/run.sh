#!/bin/bash
docker build -t lolbinarysrv .
docker run --rm -p80:80 -it lolbinarysrv
