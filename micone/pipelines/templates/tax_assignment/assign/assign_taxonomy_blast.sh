#!/usr/bin/env bash

set -e

# blast
qiime  feature-classifier classify-consensus-blast \
    --i-query ${repseq_artifact} \
    --i-reference-reads ${refseq_artifact} \
    --i-reference-taxonomy ${taxmap_artifact} \
    --p-maxaccepts ${params.blast.max_accepts} \
    --p-perc-identity ${params.blast.perc_identity} \
    --p-evalue ${params.blast.evalue} \
    --p-min-consensus ${params.blast.min_consensus} \
    --o-classification taxonomy.qza

# export the taxonomy assignment
qiime tools export \
    --input-path taxonomy.qza \
    --output-path taxonomy

cp taxonomy/taxonomy.tsv taxonomy.tsv
