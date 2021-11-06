#!/usr/bin/env bash

set -e

mkdir sequence_folder
mv ${sequence_files} sequence_folder
mv ${manifest_file} sequence_folder
mv ${sequence_metadata} sequence_folder

qiime tools import \
    --input-path sequence_folder \
    --output-path seq_artifact.qza \
    --type "${seq_type}"

qiime deblur denoise-16S \
    --i-demultiplexed-seqs seq_artifact.qza \
    --p-hashed-feature-ids \
    --p-trim-length -1 \
    --p-min-reads ${min_reads} \
    --p-min-size ${min_size} \
    --p-jobs-to-start ${ncpus} \
    --o-representative-sequences rep-seqs.qza \
    --o-table table.qza \
    --o-stats stats.qza

qiime tools export \
    --input-path rep-seqs.qza \
    --output-path rep_seqs

qiime tools export \
    --input-path table.qza \
    --output-path table

mv table/feature-table.biom ${meta.id}-${meta.run}_unhashed_otu_table.biom
mv rep_seqs/dna-sequences.fasta ${meta.id}-${meta.run}_unhashed_rep_seqs.fasta
mv ${samplemetadata_files} ${meta.id}-${meta.run}_sample_metadata.tsv
