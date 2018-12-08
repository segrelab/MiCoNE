#!/usr/bin/env python3

from qiime2 import Artifact
import re


def get_filetype(sequence_file):
    sequences = Artifact.load(sequence_file)
    raw_filetype = str(sequences.format)
    filetype = re.search(r"<class '(.+?)'>", raw_filetype).group(1)
    with open("filetype.txt", "w") as fid:
        fid.write(filetype)


if __name__ == "__main__":
    SEQUENCES = "${sequence_artifact}"
    get_filetype(SEQUENCES)
