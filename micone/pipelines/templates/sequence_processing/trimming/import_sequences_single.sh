#!/usr/bin/env bash

mkdir "${meta.id}"
cp "${manifest_file}" "${meta.id}"/
cp "${sequence_metadata}" "${meta.id}"/
cp *.fastq.gz "${meta.id}"/

qiime tools import \
    --input-path "${meta.id}" \
    --output-path "${meta.id}_sequences.qza" \
    --type "SampleData[SequencesWithQuality]"
