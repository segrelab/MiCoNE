#!/usr/bin/env #!/bin/bash

set -e

MAIN_VERSION="1.5"
VERSION="julia-1.5.3"
FNAME="$MAIN_VERSION/$VERSION-linux-x86_64.tar.gz"

URL="https://julialang-s3.julialang.org/bin/linux/x64/$FNAME"
FOLDER=/tmp/$(cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 16 | head -n 1)

mkdir "$FOLDER"
wget -O "$FOLDER/julia.tar.gz" --quiet "$URL"
tar xzf "$FOLDER/julia.tar.gz" -C "$FOLDER"

source activate micone-flashweave

cp -r "$FOLDER/$VERSION" "$CONDA_PREFIX/"
ln -s "$CONDA_PREFIX/$VERSION/bin/julia" "$CONDA_PREFIX/bin/julia"

source activate micone-flashweave
julia -e 'import Pkg; Pkg.add("FlashWeave"); Pkg.add("CSV"); Pkg.add("DataFrames"); using FlashWeave;'
