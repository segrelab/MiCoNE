#!/usr/bin/env bash

set -e

qiime tools import \
    --type  'FeatureData[Sequence]' \
    --input-path ${rep_seqs} \
    --output-path rep_seqs.qza
