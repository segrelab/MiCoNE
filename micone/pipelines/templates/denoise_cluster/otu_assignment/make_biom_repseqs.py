#!/usr/bin/env python3

import pathlib

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


def main(seqtable_file, meta_id, sample_metadata):
    seq_table = pd.read_table(seqtable_file, index_col=0)
    make_repseqs(list(seq_table.index), f"{meta_id}_unhashed_rep_seqs.fasta")
    make_biom(seq_table, f"{meta_id}_unhashed_otu_table.biom")
    sample_metadata_path = pathlib.Path(sample_metadata)
    sample_metadata_path.rename(f"{meta_id}_sample_metadata.tsv")


if __name__ == "__main__":
    SEQ_TABLE_FILE = "${seq_table_file}"
    SAMPLE_METADATA = "${samplemetadata_files}"
    META_ID = "${meta.id}-${meta.run}"
    main(SEQ_TABLE_FILE, META_ID, SAMPLE_METADATA)
