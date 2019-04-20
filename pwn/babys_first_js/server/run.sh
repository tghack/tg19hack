#!/bin/bash
docker build . -t babys_first_v8
docker run --rm -it -p 9001:9001 --name js babys_first_v8
