#!/usr/bin/env bash

qiime tools import \
  --input-path ${fasta_file} \
  --output-path seqs.qza \
  --type 'SampleData[Sequences]'

qiime vsearch dereplicate-sequences \
  --i-sequences seqs.qza \
  --o-dereplicated-table table.qza \
  --o-dereplicated-sequences rep-seqs.qza

qiime vsearch cluster-features-closed-reference \
  --i-table table.qza \
  --i-sequences rep-seqs.qza \
  --i-reference-sequences ${reference_sequences} \
  --p-perc-identity ${percent_identity} \
  --p-strand ${strand} \
  --p-threads ${ncpus} \
  --o-clustered-table table-cr.qza \
  --o-clustered-sequences rep-seqs-cr.qza \
  --o-unmatched-sequences unmatched-cr.qza

qiime tools export \
    --input-path table-cr.qza \
    --output-path table

qiime tools export \
    --input-path rep-seqs-cr.qza \
    --output-path rep_seqs

mv table/feature-table.biom ${meta.id}_unhashed_otu_table.biom
mv rep_seqs/dna-sequences.fasta ${meta.id}_unhashed_rep_seqs.fasta
mv ${samplemetadata_files} ${meta.id}_sample_metadata.tsv
