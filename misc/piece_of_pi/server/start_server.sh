#!/bin/bash
socat tcp-listen:2015,fork,reuseaddr exec:"python2 /home/tghack/run.py",stderr
