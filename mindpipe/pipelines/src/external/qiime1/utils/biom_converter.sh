#!/usr/bin/env bash
biom convert -i $biom -o ${biom.baseName}.tsv --to-tsv --header-key taxonomy --output-metadata-id "Consensus Lineage"
tail -n +2 ${biom.baseName}.tsv > otucounts.tsv
