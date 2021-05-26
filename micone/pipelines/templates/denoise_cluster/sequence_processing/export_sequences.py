#!/usr/bin/env python3

import csv
import shutil
import subprocess


def fix_manifest(manifest_file):
    data = []
    with open(manifest_file) as fid:
        header = next(fid).strip().split(",")
        for line in fid:
            if not line.startswith("#"):
                data.append(line.strip().split(","))
    header[1] = "absolute-filepath"
    for i in range(len(data)):
        fname = "demux_seqs/" + data[i][1]
        new_fname = "demux_seqs/" + data[i][0] + ".fastq.gz"
        shutil.move(fname, new_fname)
        data[i][1] = "\$PWD/" + data[i][0] + ".fastq.gz"
    with open(manifest_file, "w") as fid:
        csv_writer = csv.writer(fid, delimiter=",")
        csv_writer.writerow(header)
        csv_writer.writerows(data)


def main(demux_artifact):
    cmd = [
        "qiime",
        "tools",
        "export",
        "--input-path",
        demux_artifact,
        "--output-path",
        "demux_seqs",
    ]
    subprocess.call(cmd)
    fix_manifest("demux_seqs/MANIFEST")


if __name__ == "__main__":
    DEMUX_ARTIFACT = "${demux_artifact}"
    main(DEMUX_ARTIFACT)
