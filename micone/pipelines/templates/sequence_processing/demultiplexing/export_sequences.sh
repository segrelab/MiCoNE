#!/usr/bin/env bash

qiime tools export \
    --input-path "${demux_artifact}" \
    --output-path demux_seqs
