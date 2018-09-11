#!/usr/bin/env bash
PseudoPvals.py $correlation $bstrap $niters -o ${level}_pval.tsv -t 'two_sided'  >> sparcc.log
