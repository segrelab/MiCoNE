#!/usr/bin/env bash

pick_open_reference_otus.py \
    -i ${sequence_file} \
    -m ${picking_method} \
    -r ${references} \
    -p ${parameters} \
    -a -O ${ncpus} \
    -f -o \$PWD/
mv rep_set.fna seqs_rep_set.fasta
mv otu_table_mc2_w_tax_no_pynast_failures.biom otu_table.biom
