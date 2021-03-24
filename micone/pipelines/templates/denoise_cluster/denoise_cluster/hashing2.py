#!/usr/bin/env python2

import hashlib

from biom import load_table, Table
from biom.util import biom_open
from Bio import SeqIO
from Bio.SeqIO import FastaIO


def hash_function(seq):
    return hashlib.md5(seq.encode("utf-8")).hexdigest()


def hash_otu_table(unhashed_otu_table, seqid_hash_dict, output_file):
    table = load_table(unhashed_otu_table)
    df = table.to_dataframe(dense=True)
    seq_ids = [seqid_hash_dict[i] for i in df.index]
    df.index = seq_ids
    new_table = Table(df.values, list(df.index), list(df.columns))
    with biom_open(output_file, "w") as fid:
        new_table.to_hdf5(fid, "Constructed using qiime1 clustering")


def hash_rep_seqs(unhashed_rep_seqs, output_file):
    seqs = list(SeqIO.parse(unhashed_rep_seqs, "fasta"))
    seq_ids = []
    seqid_hash_dict = dict()
    for seq in seqs:
        hash_ = hash_function(str(seq.seq))
        seqid_hash_dict[seq.id] = hash_
        seq.id = hash_function(str(seq.seq))
        seq_ids.append(seq.id)
        seq.description = ""
        seq.name = ""
    with open(str(output_file), "w") as fid:
        fasta_writer = FastaIO.FastaWriter(fid, wrap=None)
        fasta_writer.write_file(seqs)
    return seq_ids, seqid_hash_dict


def hashing(unhashed_otu_table, unhashed_rep_seqs):
    _, seqid_hash_dict = hash_rep_seqs(unhashed_rep_seqs, "rep_seqs.fasta")
    hash_otu_table(unhashed_otu_table, seqid_hash_dict, "otu_table.biom")


if __name__ == "__main__":
    UNHASHED_OTU_TABLE = "${unhashed_otu_table}"
    UNHASHED_REP_SEQS = "${unhashed_rep_seqs}"
    hashing(UNHASHED_OTU_TABLE, UNHASHED_REP_SEQS)
