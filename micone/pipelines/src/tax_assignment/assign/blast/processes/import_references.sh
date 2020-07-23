#!/usr/bin/env bash

set -e

# import reference sequences
qiime tools import \
    --type 'FeatureData[Sequence]' \
    --input-path ${reference_sequences} \
    --output-path reference_sequences.qza

# import sequence taxonomy mapping
qiime tools import \
    --type 'FeatureData[Taxonomy]' \
    --input-format HeaderlessTSVTaxonomyFormat \
    --input-path ${tax_map} \
    --output-path tax_map.qza
