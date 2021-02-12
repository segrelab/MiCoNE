#!/usr/bin/env bash

set -e

source activate micone-spring

R -e 'library(devtools); install_github("GraceYoon/SPRING")'
