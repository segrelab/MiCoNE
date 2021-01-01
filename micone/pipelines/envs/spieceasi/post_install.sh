#!/usr/bin/env bash

set -e

source activate micone-spieceasi

export TAR=$(which tar)

R -e 'library(devtools); install_github("zdk123/SpiecEasi")'

conda install -c conda-forge r-huge=1.2.7 --yes
