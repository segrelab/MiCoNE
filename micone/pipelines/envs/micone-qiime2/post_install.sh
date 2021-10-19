#!/usr/bin/env bash

set -e

source activate micone-qiime2

pip install biopython
conda install -y -c bioconda seqtk
