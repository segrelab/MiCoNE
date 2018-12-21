#!/usr/bin/env bash

pick_closed_reference_otus.py \
  -i ${sequence_file} \
  -a -O ${ncpus} \
  -r ${sequence_reference} \
  -p ${parameters} \
  --suppress_taxonomy_assignment \
  -f -o \$PWD/

pick_rep_set.py \
  -i uclust_ref_picked_otus/seqs_otus.txt \
  -f ${sequence_file} \
  -o rep_seqs.fasta
