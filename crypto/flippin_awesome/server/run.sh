#!/bin/bash
docker build -t flippin_awesome .
docker run -it -p5000:5000 --rm flippin_awesome
