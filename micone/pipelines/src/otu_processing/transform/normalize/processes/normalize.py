#!/usr/bin/env python3

from micone import Otu


def main(
    otu_file: str,
    rm_sparse_samples: bool,
    rm_sparse_obs: bool,
    axis: str,
    count_thres: int,
    prevalence_thres: float,
    abundance_thres: float,
) -> Otu:
    otu = Otu.load_data(otu_file)
    if rm_sparse_samples:
        otu = otu.rm_sparse_samples(count_thres=count_thres)
    if rm_sparse_obs:
        otu = otu.rm_sparse_obs(
            prevalence_thres=prevalence_thres, abundance_thres=abundance_thres
        )
    return otu.normalize(axis=axis)


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
    norm_otu.write("$id" + "_normalized")
