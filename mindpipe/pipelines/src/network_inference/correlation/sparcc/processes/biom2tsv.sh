#!/usr/bin/env bash
biom convert -i $otu_file -o ${id}.txt --to-tsv
sed '1d' ${id}.txt > ${id}.tsv
