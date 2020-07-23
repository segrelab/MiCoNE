#!/usr/bin/env python3

from biom import load_table
from Bio import SeqIO


def create_seqtable(seqs, otu_table):
    otu_table_df = otu_table.to_dataframe(dense=True)
    otu_table_df.index = list(map(lambda x: seqs[x], otu_table_df.index))
    otu_table_df.to_csv("seq_table.tsv", sep="\t", index=True)


def main(rep_seqs_file, otu_file):
    seqs = {seq.id: str(seq.seq) for seq in SeqIO.parse(rep_seqs_file, "fasta")}
    otu_table = load_table(otu_file)
    create_seqtable(seqs, otu_table)


if __name__ == "__main__":
    REP_SEQS_FILE = "${repseqs_file}"
    OTU_FILE = "${otutable_file}"
    main(REP_SEQS_FILE, OTU_FILE)
