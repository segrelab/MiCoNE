#!/usr/bin/env python3

import hashlib

from biom import load_table, Table
from biom.util import biom_open
from Bio import SeqIO
from Bio.SeqIO import FastaIO


def hash_function(seq):
    return hashlib.md5(seq.encode("utf-8")).hexdigest()


def hash_otu_table(unhashed_otu_table, output_file):
    table = load_table(unhashed_otu_table)
    df = table.to_dataframe(dense=True)
    seq_ids = list(map(hash_function, df.index))
    df.index = seq_ids
    new_table = Table(df.values, list(df.index), list(df.columns))
    with biom_open(output_file, "w") as fid:
        new_table.to_hdf5(fid, "Constructed by micone in dada2 pipeline")
    return seq_ids


def hash_rep_seqs(unhashed_rep_seqs, output_file):
    seqs = list(SeqIO.parse(unhashed_rep_seqs, "fasta"))
    seq_ids = []
    for seq in seqs:
        seq.id = hash_function(str(seq.seq))
        seq_ids.append(seq.id)
        seq.description = ""
        seq.name = ""
    with open(output_file, "w") as fid:
        fasta_writer = FastaIO.FastaWriter(fid, wrap=None)
        fasta_writer.write_file(seqs)
    return seq_ids


def hashing(unhashed_otu_table, unhashed_rep_seqs):
    otu_table_ids = hash_otu_table(unhashed_otu_table, "otu_table.biom")
    rep_seq_ids = hash_rep_seqs(unhashed_rep_seqs, "rep_seqs.fasta")
    assert otu_table_ids == rep_seq_ids


if __name__ == "__main__":
    UNHASHED_OTU_TABLE = "${unhashed_otu_table}"
    UNHASHED_REP_SEQS = "${unhashed_rep_seqs}"
    hashing(UNHASHED_OTU_TABLE, UNHASHED_REP_SEQS)
