#!/usr/bin/env bash

qiime tools import \
  --input-path ${fasta_file} \
  --output-path seqs.qza \
  --type 'SampleData[Sequences]'

qiime vsearch dereplicate-sequences \
  --i-sequences seqs.qza \
  --o-dereplicated-table table.qza \
  --o-dereplicated-sequences rep-seqs.qza

qiime vsearch cluster-features-open-reference \
  --i-table table.qza \
  --i-sequences rep-seqs.qza \
  --i-reference-sequences ${ref_seqs} \
  --p-perc-identity ${percent_identity} \
  --o-clustered-table table-or.qza \
  --o-clustered-sequences rep-seqs-or.qza \
  --o-new-reference-sequences new-ref-seqs-or.qza

qiime tools export \
    --input-path table-or.qza \
    --output-path table

qiime tools export \
    --input-path rep-seqs-or.qza \
    --output-path rep_seqs

mv table/feature-table.biom ${meta.id}_unhashed_otu_table.biom
mv rep_seqs/dna-sequences.fasta ${meta.id}_unhashed_rep_seqs.fasta
mv ${samplemetadata_files} ${meta.id}_sample_metadata.tsv
