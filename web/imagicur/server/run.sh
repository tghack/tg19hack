#!/bin/bash
docker build -t misconfiguration .
docker run --rm -p8080:8080 -it misconfiguration
