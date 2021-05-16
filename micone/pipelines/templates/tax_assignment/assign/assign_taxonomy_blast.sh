#!/usr/bin/env bash

set -e

# blast
qiime  feature-classifier classify-consensus-blast \
    --i-query ${repseq_artifact} \
    --i-reference-reads ${reference_sequences} \
    --i-reference-taxonomy ${tax_map} \
    --p-maxaccepts ${max_accepts} \
    --p-perc-identity ${perc_identity} \
    --p-evalue ${evalue} \
    --p-min-consensus ${min_consensus} \
    --o-classification taxonomy.qza

# export the taxonomy assignment
qiime tools export \
    --input-path taxonomy.qza \
    --output-path taxonomy

cp taxonomy/taxonomy.tsv taxonomy.tsv
