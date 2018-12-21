#!/usr/bin/env bash

pick_open_reference_otus.py \
    -i ${sequence_file} \
    -m ${picking_method} \
    -r ${sequence_reference} \
    -p ${parameters} \
    -a -O ${ncpus} \
    --suppress_taxonomy_assignment \
    --suppress_align_and_tree \
    -f -o \$PWD/
mv rep_set.fna rep_seqs.fasta
mv otu_table_mc2.biom otu_table.biom
