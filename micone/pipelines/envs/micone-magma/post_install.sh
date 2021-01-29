#!/usr/bin/env bash

set -e

source activate micone-magma

R -e 'library(devtools); install_gitlab("arcgl/rmagma")'
