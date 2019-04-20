#!/bin/bash

set -eux

fetch v8
pushd v8
git checkout b14fdae7799e2990dd49d7c6d933ca4928b936ef
git apply < ../mad_performance.patch
git apply < ../d8_fixes.patch

gclient sync

gn gen out/foobar --args='is_debug=false target_cpu="x64" v8_target_cpu="x64" use_goma=false v8_use_external_startup_data=false'
ninja -C out/foobar d8

popd
