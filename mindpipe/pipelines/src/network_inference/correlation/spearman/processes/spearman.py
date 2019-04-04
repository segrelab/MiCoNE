#!/usr/bin/env python3

import numpy as np
import pandas as pd
from scipy.stats import spearmanr


def main(otu_file, output_file):
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
    corr_table.fillna(value=1.0, inplace=True)
    corr_table.to_csv(output_file, sep="\\t", index=True, float_format="%.4f")


if __name__ == "__main__":
    OTU_FILE = "${otu_file}"
    OUTPUT_FILE = "${otu_file.baseName.split('_otu')[0]}_corr.tsv"
    main(OTU_FILE, OUTPUT_FILE)
