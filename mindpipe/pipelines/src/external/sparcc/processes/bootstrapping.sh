#!/usr/bin/env bash
fastspar --iterations $iterations --yes \
    --otu_table $resample \
    --correlation ${resample.baseName}_corr.boot \
    --covariance ${resample.baseName}_cov.boot
