#!/usr/bin/env bash

set -e

# import reference sequences
# NOTE: qiime feature-classifier extract-reads must already be performed on the reference sequences
qiime tools import \
    --type 'FeatureData[Sequence]' \
    --input-path ${params.naive_bayes.reference_sequences} \
    --output-path reference_sequences.qza

# import sequence taxonomy mapping
qiime tools import \
    --type 'FeatureData[Taxonomy]' \
    --input-format HeaderlessTSVTaxonomyFormat \
    --input-path ${params.naive_bayes.tax_map} \
    --output-path tax_map.qza

qiime feature-classifier fit-classifier-naive-bayes \
    --i-reference-reads reference_sequences.qza \
    --i-reference-taxonomy tax_map.qza \
    --o-classifier classifier.qza
