#!/bin/bash
sudo docker build . -t counter
sudo docker run -it --rm --name counter -p 2018:2018 counter:latest

