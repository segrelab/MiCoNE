#!/usr/bin/env bash

set -e

conda activate micone-harmonies

R -e 'install.packages(c("mvnfast", "networkD3"), repo="https://mirror.las.iastate.edu/CRAN/")'
R -e 'library(devtools); install_github("shuangj00/HARMONIES", subdir = "pkg" )'
