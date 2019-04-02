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

mv rep_set.fna unhashed_rep_seqs.fasta
mv otu_table_mc2.biom unhashed_otu_table.biom
