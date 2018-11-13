#!/usr/bin/env bash

awk -F "\\t" -vOFS='\\t' 'NF{NF-=1};1' $otu_file > ${id}_otu.tsv
awk -F "\\t" '{print \$1, \$NF}' $otu_file > ${id}_lineage.txt
awk -F "\\t" 'NR==1{ s = ""; for (i=2; i<=NF-1; i++) s = s \$i " "; print s }' $otu_file > ${id}_obs.txt