#!/bin/bash

docker build . -t pi
docker run --rm -it -p 2015:2015 --pids-limit 50 pi
