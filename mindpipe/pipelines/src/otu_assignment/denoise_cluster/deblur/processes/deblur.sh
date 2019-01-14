#!/usr/bin/env bash

set -e

qiime deblur denoise-16S  \
    --i-demultiplexed-seqs ${sequence_artifact} \
    --p-trim-length -1 \
    --p-sample-stats \
    --p-min-reads ${min_reads} \
    --p-min-size ${min_size} \
    --p-jobs-to-start ${ncpus} \
    --o-representative-sequences rep_seqs.qza \
    --o-table otu_table.qza \
    --o-stats stats.qza \

qiime tools export \
    --input-path otu_table.qza \
    --output-path otu_table
mv otu_table/feature-table.biom otu_table.biom

qiime tools export \
    --input-path rep_seqs.qza \
    --output-path rep_seqs
mv rep_seqs/dna-sequences.fasta rep_seqs.fasta
