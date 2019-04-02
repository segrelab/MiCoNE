#!/usr/bin/env bash

pick_de_novo_otus.py \
  -i ${fasta_file} \
  ${parallel_option} \
  -p ${parameters} \
  -f -o \$PWD

mv rep_set/${id}_rep_set.fasta rep_seqs.fasta

mv otu_table.biom unhashed_otu_table.biom
mv rep_seqs.fasta unhashed_rep_seqs.fasta
