#!/usr/bin/env bash

set -e

URL="https://github.com/tinglab/mLDM/raw/master/mLDM_1.1.tar.gz"
FOLDER=/tmp/$(cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 16 | head -n 1)

mkdir "$FOLDER"
wget -O "$FOLDER/mldm.tar.gz" --quiet "$URL"
export MLDM_ZIP="$FOLDER/mldm.tar.gz"

source activate micone-mldm

R -e 'install.packages(c("lbfgs", "QUIC", "RcppEigen"), repos="http://archive.linux.duke.edu/cran/")'
R -e 'install.packages(Sys.getenv("MLDM_ZIP"), repos=NULL, type="source")'
