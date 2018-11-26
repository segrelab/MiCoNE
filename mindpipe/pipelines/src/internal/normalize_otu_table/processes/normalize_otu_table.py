#!/usr/bin/env python3

from minpipe import Otu


def main(otu_file: str, rm_sparse_samples: bool, rm_sparse_obs: bool) -> Otu:
    otu = Otu.load_data(otu_file)
    if rm_sparse_samples:
        otu = otu.rm_sparse_samples()
    if rm_sparse_obs:
        otu = otu.rm_sparse_obs()
    return otu.normalize()


if __name__ == "__main__":
    OTU_FILE = "$otu_file"
    AXIS = "$axis"
    RM_SPARSE_SAMPLES = $rm_sparse_samples
    COUNT_THRES = $count_thres
    RM_SPARSE_OBS = $rm_sparse_obs
    PREVALENCE_THRES = $prevalence_thres
    ABUNDANCE_THRES = $abundance_thres
    norm_otu = main(
        OTU_FILE,
        RM_SPARSE_SAMPLES,
        RM_SPARSE_OBS,
        AXIS,
        COUNT_THRES,
        PREVALENCE_THRES,
        ABUNDANCE_THRES,
    )
    norm_otu.write("norm_otu.biom")
