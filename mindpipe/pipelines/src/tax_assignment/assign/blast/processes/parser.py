#!/usr/bin/env python3

from Bio.Blast.NCBIXML import parse
import pandas as pd


# TODO: Add consensus/scoring function
def scoring():
    pass


# TODO: Might want to parallelize this
def parser(blast_file, tax_map, n_hits):
    map_file = tax_map
    map_data = pd.read_table(map_file, index_col=0, header=None)
    tax_list = []
    with open(blast_file, "r") as fid:
        for record in parse(fid):
            for description in record.descriptions:
                id_ = description.accession
                tax = map_data.loc[id_][1]
                tax_list.append({"id": record.query, "Taxon": tax})
                break
    return pd.DataFrame(tax_list)


if __name__ == "__main__":
    BLAST_FILE = "${blast_output}"
    TAX_MAP = "${tax_map}"
    N_HITS = int("${n_hits}")
    df = parser(BLAST_FILE, TAX_MAP, N_HITS)
    df.set_index("id", inplace=True)
    df.to_csv("tax_assignment.tsv", index=True, sep="\t")
