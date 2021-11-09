#!/usr/bin/env python3

import pathlib
import multiprocessing as mp

import numpy as np
import pandas as pd
from scipy.stats import spearmanr


def spearman(otu_file, output_file):
    otu_table = pd.read_table(otu_file, index_col=0)
    data = otu_table.values
    n = otu_table.shape[0]
    index = otu_table.index
    corr_data = np.zeros((n, n), dtype=np.float)
    for i in range(n):
        for j in range(i, n):
            if i == j:
                corr_data[i][j] = 1.0
            else:
                corr, _ = spearmanr(data[i, :], data[j, :])
                corr_data[i][j] = corr
                corr_data[j][i] = corr
    corr_table = pd.DataFrame(data=corr_data, index=index, columns=index)
    corr_table.fillna(value=0.0, inplace=True)
    corr_table.to_csv(output_file, sep="\\t", index=True, float_format="%.4f")


def main(id_, otu_file, bootstrap_files, ncpus):
    output_file = f"{id_}_corr.tsv"
    args = [(otu_file, output_file)]
    for i, bootstrap_file in enumerate(bootstrap_files):
        output_file = bootstrap_file.name.replace("_otu.boot", "_corr.boot")
        args.append((bootstrap_file, output_file))
    with mp.Pool(processes=ncpus) as pool:
        pool.starmap(spearman, args)


if __name__ == "__main__":
    ID_ = "${meta.id}"
    OTU_FILE = pathlib.Path("${otu_file}")
    BOOTSTRAP_FILES = pathlib.Path().glob("*_otu.boot")
    NCPUS = int("${ncpus}")
    main(ID_, OTU_FILE, BOOTSTRAP_FILES, NCPUS)
