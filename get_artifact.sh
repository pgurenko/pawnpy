#!/bin/bash

DOWNLOAD_URI=https://github.com/pgurenko/pawnpy/releases/download/$(git describe)
curl -L $DOWNLOAD_URI/$1 -o ./pawnpy/$1
