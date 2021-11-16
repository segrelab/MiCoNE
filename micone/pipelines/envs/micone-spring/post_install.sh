#!/usr/bin/env bash

set -e

source activate micone-spring

R -e 'devtools::install_github("irinagain/mixedCCA")'
R -e 'devtools::install_github("GraceYoon/SPRING")'
