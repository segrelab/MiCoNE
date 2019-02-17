#!/usr/bin/env bash
fastspar --iterations $iterations --yes \
    --otu_table $otu_file \
    --correlation ${level}_corr.tsv \
    --covariance ${level}_cov.tsv
