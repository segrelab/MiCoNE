#!/usr/bin/env python3

from functools import partial
import os
import pathlib
import multiprocessing as mp
import shutil
import subprocess


def trim(sequence, cutadapt_args):
    cmd = ["cutadapt"]
    cmd.extend(cutadapt_args)
    fname = sequence.rsplit("/")[-1]
    output_fname = "trimmed/" + fname
    cmd.append("--output={}".format(output_fname))
    cmd.append(sequence)
    subprocess.call(cmd)


def main(sequence_glob, trim_cmd, ncpus):
    os.mkdir("trimmed")
    shutil.copy("MANIFEST", "trimmed/MANIFEST")
    cutadapt_args = []
    with open(trim_cmd) as fid:
        for line in fid:
            cutadapt_args.append(line.strip())
    folder, glob = sequence_glob.rsplit("/", 1)
    sequences = list(str(p) for p in pathlib.Path(folder).glob(glob))
    trim_func = partial(trim, cutadapt_args=cutadapt_args)
    with mp.Pool(processes=ncpus) as pool:
        pool.map(trim_func, sequences)


if __name__ == "__main__":
    SEQUENCE_GLOB = "${sequence_glob}"
    TRIM_CMD = "${trim_cmd}"
    NCPUS = $ncpus
    main(SEQUENCE_GLOB, TRIM_CMD, NCPUS)
