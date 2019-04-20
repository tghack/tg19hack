#!/bin/bash
docker build -t wizardschat .
docker run --rm --name=wizardschat -p8800:8800 -it wizardschat
