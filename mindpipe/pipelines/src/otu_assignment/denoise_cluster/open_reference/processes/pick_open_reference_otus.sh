#!/usr/bin/env bash

pick_open_reference_otus.py \
    -i ${fasta_file} \
    -m ${picking_method} \
    -r ${sequence_16s_reference} \
    ${parameters_option} \
    ${parallel_option} \
    --suppress_taxonomy_assignment \
    --suppress_align_and_tree \
    -f -o \$PWD/

mv rep_set.fna rep_seqs.fasta
mv otu_table_mc2.biom otu_table.biom
