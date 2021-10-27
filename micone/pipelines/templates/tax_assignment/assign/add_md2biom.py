#!/usr/bin/env python3

import os

from biom import load_table
from biom.util import biom_open
import pandas as pd


HEADERS = ["Kingdom", "Phylum", "Class", "Order", "Family", "Genus", "Species"]


def tax_splitter(full_tax):
    tax_list = [tax.strip().split("__")[-1] for tax in full_tax.Taxon.split(";")]
    tax_list = [
        t.replace("'", "").replace("=", "").replace("[", "").replace("]", "")
        for t in tax_list
    ]
    tax_list.extend([""] * (len(HEADERS) - len(tax_list)))
    return pd.Series(data=tax_list, index=HEADERS)


def main(otu_table_file, tax_assignment_file, sample_metadata_file):
    otu_table = load_table(otu_table_file)
    if os.path.splitext(sample_metadata_file)[1] == "csv":
        sample_metadata = pd.read_csv(sample_metadata_file, index_col=0, comment="#")
    else:
        sample_metadata = pd.read_table(sample_metadata_file, index_col=0, comment="#")
    tax_assignment = pd.read_table(tax_assignment_file, index_col=0)
    obs_metadata = tax_assignment[["Taxon"]].apply(tax_splitter, axis=1)
    for index in otu_table.ids("observation"):
        if index not in obs_metadata.index:
            obs_metadata.loc[index] = [""] * len(HEADERS)
    otu_table.del_metadata(axis="observation")
    otu_table.add_metadata(obs_metadata.to_dict(orient="index"), axis="observation")
    otu_table.del_metadata(axis="sample")
    otu_table.add_metadata(sample_metadata.to_dict(orient="index"), axis="sample")
    with biom_open("otu_table_wtax.biom", "w") as fid:
        otu_table.to_hdf5(fid, "Constructed using the micone pipeline")


if __name__ == "__main__":
    OTU_TABLE = "${otu_table_file}"
    TAX_ASSIGNMENT = "${tax_assignment}"
    SAMPLE_METADATA = "${sample_metadata_file}"
    main(OTU_TABLE, TAX_ASSIGNMENT, SAMPLE_METADATA)
