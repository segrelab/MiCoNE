#!/usr/bin/env bash
fastspar --iterations $iterations --yes \
    --otu_table $otu_file \
    --correlation ${id}_corr.tsv \
    --covariance ${id}_cov.tsv
