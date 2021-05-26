#!/usr/bin/env bash

set -e

mkdir sequence_folder
mv ${sequence_files} sequence_folder
mv ${manifest_file} sequence_folder

deblur workflow \
    --seqs-fp  sequence_folder \
    --output-dir deblur_output \
    -t -1 \
    --left-trim-length 0 \
    --min-reads ${min_reads} \
    --min-size ${min_size} \
    --jobs-to-start ${ncpus} \
    --keep-tmp-files

# Build otu table and rep seqs for the step before chimera checking
mkdir otu_table
deblur build-biom-table \
    --min-reads ${min_reads} \
    --file_type .trim.derep.no_artifacts.msa.deblur \
    deblur_output/deblur_working_dir \
    otu_table

mv otu_table/all.biom unhashed_otu_table.biom
mv otu_table/all.seq.fa unhashed_rep_seqs.fasta
