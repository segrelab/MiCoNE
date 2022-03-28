#!/usr/bin/env python3

from micone import Otu


def main(
    otu_file: str,
    rm_sparse_samples: str,
    rm_sparse_obs: str,
    axis: str,
    count_thres: int,
    prevalence_thres: float,
    abundance_thres: float,
    obssum_thres: float,
) -> Otu:
    otu = Otu.load_data(otu_file)
    if rm_sparse_samples == "true":
        otu = otu.rm_sparse_samples(count_thres=count_thres)
    if rm_sparse_obs == "true":
        otu = otu.rm_sparse_obs(
            prevalence_thres=prevalence_thres,
            abundance_thres=abundance_thres,
            obssum_thres=obssum_thres,
        )
    else:
        n_samples = otu.otu_data.shape[1]
        otu = otu.rm_sparse_obs(
            prevalence_thres=2 / n_samples, abundance_thres=0.001, obssum_thres=10
        )
    if axis != "None":
        otu_norm = otu.normalize(axis=axis)
    else:
        otu_norm = otu
    return otu_norm


if __name__ == "__main__":
    OTU_FILE = "${otu_file}"
    AXIS = "${axis}"
    RM_SPARSE_SAMPLES = "${rm_sparse_samples}"
    COUNT_THRES = int("${count_thres}")
    RM_SPARSE_OBS = "${rm_sparse_obs}"
    PREVALENCE_THRES = float("${prevalence_thres}")
    ABUNDANCE_THRES = float("${abundance_thres}")
    norm_otu = main(
        OTU_FILE,
        RM_SPARSE_SAMPLES,
        RM_SPARSE_OBS,
        AXIS,
        COUNT_THRES,
        PREVALENCE_THRES,
        ABUNDANCE_THRES,
        OBSSUM_THRES,
    )
    norm_otu.write("${meta.id}" + "_normalized_filtered")
