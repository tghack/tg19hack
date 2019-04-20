#!/bin/bash
docker build -t rekeygen .
docker run --rm -p2222:2222 -it rekeygen
