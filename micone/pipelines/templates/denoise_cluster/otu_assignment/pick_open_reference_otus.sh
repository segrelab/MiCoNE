#!/usr/bin/env bash

pick_open_reference_otus.py \
    -i ${fasta_file} \
    -m ${picking_method} \
    -r ${reference_sequences} \
    -p ${parameters} \
    ${parallel_option} \
    --suppress_taxonomy_assignment \
    --suppress_align_and_tree \
    -f -o \$PWD

mv otu_table_mc2.biom ${meta.id}_unhashed_otu_table.biom
mv rep_set.fna ${meta.id}_unhashed_rep_seqs.fasta
mv ${samplemetadata_files} ${meta.id}_sample_metadata.tsv
