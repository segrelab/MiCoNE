#!/usr/bin/env python3

from functools import partial
import os
import pathlib
import multiprocessing as mp
import shutil
import subprocess


def trim(sequence, cutadapt_args, adapters):
    front_adapter = adapters[0]
    tail_adapter = adapters[1]
    cmd = ["cutadapt"]
    if front_adapter:
        cmd.append("--front={}".format(front_adapter))
    if tail_adapter:
        cmd.append("--adapter={}".format(tail_adapter))
    cmd.extend(cutadapt_args)
    fname = sequence.rsplit("/")[-1]
    output_fname = "trimmed/" + fname
    cmd.append("--output={}".format(output_fname))
    cmd.append(sequence)
    subprocess.call(cmd)


def main(sequence_glob, trim_cmd, ncpus, adapters):
    os.mkdir("trimmed")
    shutil.copy("MANIFEST", "trimmed/MANIFEST")
    cutadapt_args = []
    with open(trim_cmd) as fid:
        for line in fid:
            cutadapt_args.append(line.strip())
    folder = pathlib.Path()
    sequences = list(str(p) for p in folder.glob(sequence_glob))
    trim_func = partial(trim, cutadapt_args=cutadapt_args, adapters=adapters)
    with mp.Pool(processes=ncpus) as pool:
        pool.map(trim_func, sequences)


if __name__ == "__main__":
    SEQUENCE_GLOB = "*.fastq.gz"
    TRIM_CMD = "${trim_cmd}"
    NCPUS = $ncpus
    ADAPTERS = ["${front_adapter}", "${tail_adapter}"]
    main(SEQUENCE_GLOB, TRIM_CMD, NCPUS, ADAPTERS)
