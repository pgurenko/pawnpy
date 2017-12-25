#!/bin/bash

DOWNLOAD_URI=https://github.com/pgurenko/pawnpy/releases/download/$(git describe)
curl $DOWNLOAD_URI/libpawnpy.linux.x64.so -o ./pawnpy/libpawnpy.linux.x64.so
curl $DOWNLOAD_URI/pawncc.linux.x64 -o ./pawnpy/pawncc.linux.x64

tar -zcvf pawnpy-$(git describe).tar.gz setup.py pawnpy/*.py pawnpy/*.so pawnpy/pawncc*