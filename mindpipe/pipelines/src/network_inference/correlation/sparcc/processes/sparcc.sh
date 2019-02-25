#!/usr/bin/env bash
fastspar --iterations $iterations --yes \
    --otu_table $otu_file \
    --correlation ${otu_file.baseName}_corr.tsv \
    --covariance ${otu_file.baseName}_cov.tsv \
    --threads ${threads}
