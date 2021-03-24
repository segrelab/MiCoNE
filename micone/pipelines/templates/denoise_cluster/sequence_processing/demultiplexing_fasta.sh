#!/usr/bin/env bash

split_libraries.py -m $mapping -f $sequences -q $qualities -w ${params.demultiplexing_454.qual_score_window}
