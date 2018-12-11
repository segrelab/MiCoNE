#!/usr/bin/env bash

set -e

FNAME="fastspar-0.0.9_linux"

URL="https://github.com/scwatts/fastspar/releases/download/v0.0.9/$FNAME.tar.gz"
FOLDER=/tmp/$(cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 16 | head -n 1)

mkdir "$FOLDER"
mkdir "$FOLDER/fastspar"

wget -O "$FOLDER/fastspar.tar.gz" "$URL"
tar xvzf "$FOLDER/fastspar.tar.gz" -C "$FOLDER"

source activate mindpipe-sparcc

cp $FOLDER/$FNAME/fastspar* "$CONDA_PREFIX/bin/"
