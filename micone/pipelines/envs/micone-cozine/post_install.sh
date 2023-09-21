#!/usr/bin/env bash

set -e

conda activate micone-cozine

R -e 'BiocManager::install("amcdavid/HurdleNormal")'
R -e 'library(devtools); install_github("MinJinHa/COZINE")'
