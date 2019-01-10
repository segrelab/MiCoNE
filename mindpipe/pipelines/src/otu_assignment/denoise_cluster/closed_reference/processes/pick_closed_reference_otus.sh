#!/usr/bin/env bash

pick_closed_reference_otus.py \
  -i ${fasta_file} \
  ${parallel_option} \
  -r ${sequence_16s_reference} \
  ${parameters_option} \
  --suppress_taxonomy_assignment \
  -f -o \$PWD/

pick_rep_set.py \
  -i uclust_ref_picked_otus/${id}_otus.txt \
  -f ${fasta_file} \
  -o rep_seqs.fasta
