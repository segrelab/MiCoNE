#!/usr/bin/env bash

mkdir sequence_folder
mv ${sequence_files} sequence_folder
mv ${manifest_file} sequence_folder
mv ${sequence_metadata} sequence_folder

qiime tools import \
    --input-path sequence_folder \
    --output-path seq_artifact.qza \
    --type "SampleData[PairedEndSequencesWithQuality]"

qiime vsearch join-pairs \
    --i-demultiplexed-seqs seq_artifact.qza \
    --o-joined-sequences joined_artifact.qza

qiime tools export \
    --input-path joined_artifact.qza \
    --output-path joined_reads
