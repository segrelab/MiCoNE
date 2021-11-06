#!/usr/bin/env python3

import hashlib
import pathlib

from biom import load_table, Table
from biom.util import biom_open
from Bio import SeqIO
from Bio.SeqIO import FastaIO
import pandas as pd


def hash_function(seq):
    return hashlib.md5(seq.encode("utf-8")).hexdigest()


def hash_otu_table(unhashed_otu_table, seqid_hash_dict):
    table = load_table(unhashed_otu_table)
    df = table.to_dataframe(dense=True)
    seq_ids = [seqid_hash_dict[i] for i in df.index]
    df.index = seq_ids
    return df


def hash_rep_seqs(unhashed_rep_seqs, rep_seq_ids):
    seqs_all = list(SeqIO.parse(unhashed_rep_seqs, "fasta"))
    seqs = []
    seqid_hash_dict = dict()
    for seq in seqs_all:
        hash_ = hash_function(str(seq.seq))
        seqid_hash_dict[seq.id] = hash_
        seq.id = hash_function(str(seq.seq))
        seq.description = ""
        seq.name = ""
        if seq.id not in rep_seq_ids:
            rep_seq_ids.add(hash_)
            seqs.append(seq)
    return seqs, seqid_hash_dict


def hashing(unhashed_otu_table_list, unhashed_rep_seqs_list, sample_metadata_list):
    otu_df_list = []
    rep_seq_ids = set()
    seqs = []
    for unhashed_rep_seqs, unhashed_otu_table in zip(
        unhashed_rep_seqs_list, unhashed_otu_table_list
    ):
        seq, seqid_hash_dict = hash_rep_seqs(unhashed_rep_seqs, rep_seq_ids)
        seqs.extend(seq)
        otu_df_list.append(hash_otu_table(unhashed_otu_table, seqid_hash_dict))
    # Merge OTU table
    otu_df = pd.concat(otu_df_list, join="outer", axis=1)
    otu_df.fillna(0.0, inplace=True)
    otu_table = Table(otu_df.values, list(otu_df.index), list(otu_df.columns))
    otu_table_ids = set(otu_df.index)
    assert otu_table_ids == rep_seq_ids
    assert len(otu_df.index) == len(rep_seq_ids)
    # Merge rep seqs
    # Merge sample metadata
    sample_metadata = pd.concat(
        [pd.read_csv(s, sep="\\t") for s in sample_metadata_list]
    )

    # Write files
    sample_metadata.to_csv("sample_metadata.tsv", sep="\\t", index=False)
    with biom_open("otu_table.biom", "w") as fid:
        otu_table.to_hdf5(fid, "Constructed using qiime2 clustering")
    with open("rep_seqs.fasta", "w") as fid:
        fasta_writer = FastaIO.FastaWriter(fid, wrap=None)
        fasta_writer.write_file(seqs)


if __name__ == "__main__":
    UNHASHED_OTU_TABLE_LIST = sorted(pathlib.Path().glob("*unhashed_otu_table.biom"))
    UNHASHED_REP_SEQS_LIST = sorted(pathlib.Path().glob("*unhashed_rep_seqs.fasta"))
    SAMPLE_METADATA_LIST = sorted(pathlib.Path().glob("*sample_metadata.tsv"))
    hashing(UNHASHED_OTU_TABLE_LIST, UNHASHED_REP_SEQS_LIST, SAMPLE_METADATA_LIST)
