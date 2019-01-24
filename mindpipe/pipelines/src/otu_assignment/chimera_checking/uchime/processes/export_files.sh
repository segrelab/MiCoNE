#!/usr/bin/env bash

set -e

# Export otu table
qiime tools export \
    --input-path ${otutable_nonchimeric} \
    --output-path otu_table

# Export representative sequences
qiime tools export \
    --input-path ${repseqs_nonchimeric} \
    --output-path rep_seqs

mv otu_table/feature-table.biom otu_table.biom
mv rep_seqs/dna-sequences.fasta rep_seqs.fasta
