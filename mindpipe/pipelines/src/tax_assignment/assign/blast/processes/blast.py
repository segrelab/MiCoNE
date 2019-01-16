#!/usr/bin/env python3

import os

from Bio.Blast.Applications import NcbiblastnCommandline

os.environ["BLASTDB"] = "${blast_db}"


# How can we parallelize this?
# Separate into smaller fasta files and then use multiprocessing
def blast(query, db, evalue_cutoff):
    cline = NcbiblastnCommandline(
        query=query,
        db=db,
        strand="plus",
        evalue=evalue_cutoff,
        out="blast_output.xml",
        outfmt=5,
    )
    stdout, stderr = cline()


if __name__ == "__main__":
    QUERY = "${rep_seqs}"
    DB = "${blast_db.baseName}"
    EVALUE_CUTOFF = float("${evalue_cutoff}")
    blast(QUERY, DB, EVALUE_CUTOFF)
