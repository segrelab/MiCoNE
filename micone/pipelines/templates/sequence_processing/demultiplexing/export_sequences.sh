#!/usr/bin/env bash

qiime tools export \
    --input-path "${demux_artifact}" \
    --output-path demux_seqs

if [[ '${sample_filter}' ]]; then
    cd demux_seqs || exit
    ls -1 | grep -v '${sample_filter}' | xargs rm -f
    mv MANIFEST MANIFEST_OLD
    sed '/sample-id\|${sample_filter}/!d' MANIFEST_OLD >MANIFEST
    rm MANIFEST_OLD
fi
