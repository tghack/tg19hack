#!/bin/bash
set -eu
docker build -t wandshop .
docker run --rm -p8000:8000 wandshop
