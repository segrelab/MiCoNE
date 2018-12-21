#!/usr/bin/env bash

pick_de_novo_otus.py \
  -i ${sequence_file} \
  -a -O ${ncpus} \
  -p ${parameters} \
  -f -o \$PWD/

mv rep_set/seqs_rep_set.fasta rep_seqs.fasta
