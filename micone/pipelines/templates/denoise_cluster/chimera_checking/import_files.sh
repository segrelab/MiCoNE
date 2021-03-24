#!/usr/bin/env bash

set -e

# Import biom file
qiime tools import \
    --input-path ${otu_table} \
    --type 'FeatureTable[Frequency]' \
    --input-format BIOMV210Format \
    --output-path otu_table.qza

# Import representative sequences
qiime tools import \
    --input-path ${rep_seqs} \
    --type 'FeatureData[Sequence]' \
    --output-path rep_seqs.qza
