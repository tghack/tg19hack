#!/bin/bash
socat tcp-listen:2222,fork,reuseaddr exec:"python3 /home/tghack/server.py",stderr
