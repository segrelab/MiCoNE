#!/usr/bin/env bash

pick_open_reference_otus.py -i ${sequence_list} \
                            -m ${picking_method} \
                            -r ${references} \
                            -p ${parameters} \
                            -a -O ${ncpus} \
                            -s ${percent_subsample} \
                            -f -o \$PWD/

