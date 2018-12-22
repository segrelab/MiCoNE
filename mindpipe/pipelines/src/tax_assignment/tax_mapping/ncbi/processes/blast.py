#!/usr/bin/env python3

import os

from Bio.Blast.Applications import NcbiblastnCommandline

os.environ["BLASTDB"] = "${blastdb}"


def blast(query, db):
    cline = NcbiblastnCommandline(
        query=query,
        db=db,
        strand="plus",
        evalue=1e-20,
        out="blast_output.xml",
        outfmt=5,
    )
    stdout, stderr = cline()


if __name__ == "__main__":
    QUERY = "${query}"
    DB = "${db}"
    blast(QUERY, DB)
