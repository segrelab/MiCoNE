#!/usr/bin/env bash

pick_de_novo_otus.py \
  -i ${fasta_file} \
  ${parallel_option} \
  ${parameters_option} \
  -f -o \$PWD/

mv rep_set/${id}_rep_set.fasta rep_seqs.fasta
