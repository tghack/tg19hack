#!/bin/bash
docker build . -t piece-of-pi

# Run and compile qemu arm binary. Copy binary to vm/ folder
docker run -it --name piece-of-pi piece-of-pi
docker cp piece-of-pi:/opt/qemu-system-arm vm/
docker rm piece-of-pi
