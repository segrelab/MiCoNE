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
  --i-reference-sequences ${reference_sequences} \
  --p-perc-identity ${percent_identity} \
  --p-strand ${strand} \
  --p-threads ${ncpus} \
  --o-clustered-table table-or.qza \
  --o-clustered-sequences rep-seqs-or.qza \
  --o-new-reference-sequences new-ref-seqs-or.qza

qiime tools export \
    --input-path table-or.qza \
    --output-path table

qiime tools export \
    --input-path rep-seqs-or.qza \
    --output-path rep_seqs

mv table/feature-table.biom ${meta.id}-${meta.run}_unhashed_otu_table.biom
mv rep_seqs/dna-sequences.fasta ${meta.id}-${meta.run}_unhashed_rep_seqs.fasta
mv ${samplemetadata_files} ${meta.id}-${meta.run}_sample_metadata.tsv
