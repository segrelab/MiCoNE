#!/usr/bin/env python3


from Bio import Entrez
from Bio.Blast.NCBIXML import parse
import pandas as pd

Entrez.email = "${email}"


def parser(blast_file: str, n_hits: int):
    tax_list = []
    with open(blast_file, "r") as fid:
        for record in parse(fid):
            # QUESTION: Do we want to verify evalue again? (use description.e)
            # Do we want to use evalue to calculate the scores?
            # We want to limit the number of blast hits we query
            for description in record.descriptions:
                id_ = description.accession
                handle = Entrez.esummary(db="nucleotide", id=id_)
                summary = Entrez.read(handle)
                taxid = summary[0]["TaxId"]
                tax_list.append({"id": record.query, "taxid": taxid})
                handle.close()
                break
    return pd.DataFrame(tax_list)


if __name__ == "__main__":
    BLAST_FILE = "${blast_output}"
    df = parser(BLAST_FILE)
    df.to_csv("taxonomy.csv")
