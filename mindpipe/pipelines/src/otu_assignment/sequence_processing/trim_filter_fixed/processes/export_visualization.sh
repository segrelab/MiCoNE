#!/usr/bin/env bash

qiime demux summarize \
    --i-data ${sequence_artifact} \
    --p-n ${seq_samplesize} \
    --o-visualization quality_summary.qzv


qiime tools export \
    --input-path quality_summary.qzv \
    --output-path output
