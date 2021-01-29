#!/usr/bin/env bash

set -e

source activate micone-mldm

R -e 'install.packages(c("lbfgs", "RcppEigen"), repos="http://archive.linux.duke.edu/cran/")'
R -e 'install.packages("https://cran.r-project.org/src/contrib/Archive/QUIC/QUIC_1.1.1.tar.gz", repos=NULL, type="source")'
R -e 'install.packages("https://github.com/tinglab/mLDM/raw/master/mLDM_1.1.tar.gz", repos=NULL, type="source")'
