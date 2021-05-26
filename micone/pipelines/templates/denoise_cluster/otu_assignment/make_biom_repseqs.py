#!/usr/bin/env python3

from biom import Table
from biom.util import biom_open
import pandas as pd


def make_repseqs(seqs, output_file):
    with open(output_file, "w") as fid:
        for i, seq in enumerate(seqs):
            fid.write(f">Seq{i}\\n")
            fid.write(seq)
            fid.write("\\n")


def make_biom(seq_table, output_file):
    new_table = Table(seq_table.values, list(seq_table.index), list(seq_table.columns))
    with biom_open(output_file, "w") as fid:
        new_table.to_hdf5(fid, "Constructucted by micone in dada2 pipeline")


def main(seqtable_file):
    seq_table = pd.read_table(seqtable_file, index_col=0)
    make_repseqs(list(seq_table.index), "unhashed_rep_seqs.fasta")
    make_biom(seq_table, "unhashed_otu_table.biom")


if __name__ == "__main__":
    SEQ_TABLE_FILE = "${seq_table_file}"
    main(SEQ_TABLE_FILE)
