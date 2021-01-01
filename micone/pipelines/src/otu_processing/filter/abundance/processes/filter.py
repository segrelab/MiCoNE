#!/usr/bin/env python3

# Script that filters samples and observations based on abundance

import os

from micone import Otu


def main(otu_file, count_thres, prevalence_thres, abundance_thres):
    otu_data = Otu.load_data(otu_file)
    filtered_otu_data = otu_data.rm_sparse_obs(
        prevalence_thres, abundance_thres
    ).rm_sparse_samples(count_thres)
    fname, _ = os.path.splitext(otu_file)
    filtered_otu_data.write(f"{fname}_filtered", file_type="biom")


if __name__ == "__main__":
    OTU_FILE = "${otu_file}"
    COUNT_THRES = int("${count_thres}")
    PREVALENCE_THRES = float("${prevalence_thres}")
    ABUNDANCE_THRES = float("${abundance_thres}")
    main(OTU_FILE, COUNT_THRES, PREVALENCE_THRES, ABUNDANCE_THRES)
