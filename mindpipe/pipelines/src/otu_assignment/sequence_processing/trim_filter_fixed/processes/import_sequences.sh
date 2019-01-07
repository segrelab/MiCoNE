#!/usr/bin/env bash

mkdir sequence_folder
mv ${sequence_files} sequence_folder
mv ${manifest_file} sequence_folder

cd sequence_folder
qiime tools import \
    --type 'SampleData[SequenceWithQuality]' \
    --input-path MANIFEST \
    --input-format SingleEndFastqManifestPhred33 \
    --output-path ${id}_sequences.qza
