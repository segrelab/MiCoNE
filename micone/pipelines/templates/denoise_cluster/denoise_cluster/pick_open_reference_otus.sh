#!/usr/bin/env bash

pick_open_reference_otus.py \
    -i ${fasta_file} \
    -m ${params.open_reference.picking_method} \
    -r ${params.open_reference.reference_sequences} \
    -p ${params.open_reference.parameters} \
    ${parallel_option} \
    --suppress_taxonomy_assignment \
    --suppress_align_and_tree \
    -f -o \$PWD

mv rep_set.fna unhashed_rep_seqs.fasta
mv otu_table_mc2.biom unhashed_otu_table.biom
