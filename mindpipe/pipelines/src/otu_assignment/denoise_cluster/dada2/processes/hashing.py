#!/usr/bin/env python3

import hashlib

from biom import load_table, Table
from biom.util import biom_open
from Bio import SeqIO


def hash_function(seq):
    return hashlib.md5(seq.encode("utf-8")).hexdigest()


def hash_otu_table(unhashed_otu_table, output_file):
    table = load_table(unhashed_otu_table)
    df = table.to_dataframe(dense=True)
    df.index = list(map(hash_function, df.index))
    new_table = Table(df.values, list(df.index), list(df.columns))
    with biom_open(output_file, "w") as fid:
        new_table.to_hdf5(fid, "Constructucted by mindpipe in dada2 pipeline")


def hash_rep_seqs(unhashed_rep_seqs, output_file):
    seqs = list(SeqIO.parse(unhashed_rep_seqs, "fasta"))
    for seq in seqs:
        seq.id = hash_function(seq.id)
        seq.description = ""
        seq.name = ""
    SeqIO.write(seqs, output_file, "fasta")


def hashing(unhashed_otu_table, unhashed_rep_seqs):
    hash_otu_table(unhashed_otu_table, "otu_table.biom")
    hash_rep_seqs(unhashed_rep_seqs, "rep_seqs.fasta")


if __name__ == "__main__":
    UNHASHED_OTU_TABLE = "${unhashed_otu_table}"
    UNHASHED_REP_SEQS = "${unhashed_rep_seqs}"
    hashing(UNHASHED_OTU_TABLE, UNHASHED_REP_SEQS)
