#!/bin/bash

docker build . -t wand-shop
docker run --rm -it -p 4001:4001 wand-shop
