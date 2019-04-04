#!/usr/bin/env bash

set -e

source activate mindpipe-magma

export TAR=$(which tar)

R -e 'library(devtools); install_github("zdk123/SpiecEasi"); install_gitlab("arcgl/rmagma")'
