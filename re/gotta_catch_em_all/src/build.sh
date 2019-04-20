#!/bin/bash

echo "[+] building docker container!"
docker build . -t pokered

echo "[+] running container"
docker run --rm --name pokered -t -d pokered

echo "[+] copying ROM"
docker cp pokered:/opt/pokered/pokered.gbc ./pokered.gbc
docker cp pokered:/opt/pokered/pokered.sym ./pokered.sym

echo "[+] killing container"
docker kill pokered

echo "[+] patching ROM"
bspatch pokered.gbc pokered_patched.gbc pokered.patch

echo "[+] done!"
