#!/usr/bin/env python3

import pathlib
import os
import subprocess


def convert(data):
    sample_name, file_name = data
    fasta_file = "fasta/" + sample_name + ".fasta"
    with open(fasta_file, "w") as fid:
        cmd = ["seqtk", "seq", "-a", file_name]
        subprocess.call(cmd, stdout=fid)
    return fasta_file


def merge(fasta_files, output_file):
    with open(output_file, "w") as wid:
        for fasta_file in fasta_files:
            with open(fasta_file) as rid:
                sample_name = pathlib.Path(fasta_file).stem
                count = 0
                for line in rid:
                    if line.startswith(">"):
                        wid.write(
                            ">{0}_{1} {2}".format(sample_name, str(count), line[1:])
                        )
                    else:
                        wid.write(line)
                    count += 1


def main(manifest_file, dataset_name):
    os.mkdir("fasta")
    data = []
    with open(manifest_file) as fid:
        _ = next(fid).strip().split(",")
        for line in fid:
            if not line.startswith("#"):
                sample_name, file_location, _ = line.strip().split(",")
                data.append((sample_name, file_location.rsplit("/")[-1]))
    fasta_files = map(convert, data)
    merged_fasta_file = dataset_name + ".fasta"
    merge(fasta_files, merged_fasta_file)


if __name__ == "__main__":
    DATASET_NAME = "${meta.id}"
    MANIFEST_FILE = "${manifest_file}"
    main(MANIFEST_FILE, DATASET_NAME)
