#!/usr/bin/env bash

set -e

# Import biom file
qiime tools import \
    --input-path ${otutable_file} \
    --type 'FeatureTable[Frequency]' \
    --input-format BIOMV210Format \
    --output-path otu_table.qza

# Import representative sequences
qiime tools import \
    --input-path ${repseqs_file} \
    --type 'FeatureData[Sequence]' \
    --output-path rep_seqs.qza
