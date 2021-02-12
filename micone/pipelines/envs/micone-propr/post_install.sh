#!/usr/bin/env bash

set -e

source activate micone-propr

R -e 'library(devtools); install_github("tpq/propr")'
