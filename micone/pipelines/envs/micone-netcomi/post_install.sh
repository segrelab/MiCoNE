#!/usr/bin/env bash

set -e

source activate micone-netcomi

R -e 'devtools::install_github("stefpeschel/NetCoMi", dependencies = TRUE, repos = c("https://cloud.r-project.org/", BiocManager::repositories())); NetCoMi::installNetCoMiPacks()'
