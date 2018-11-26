#!/usr/bin/env nextflow

def output_dir = file(params.output_dir)
def otudata = params.otudata

def axis = params.axis
def count_thres = params.count_thres
def prevalence_thres = params.prevalence_thres
def abundance_thres = params.abundance_thres
def rm_sparse_obs = params.rm_sparse_obs
def rm_sparse_samples = params.rm_sparse_samples
def rm_sparse_obs = params.rm_sparse_obs
def rm_sparse_samples = params.rm_sparse_samples

Channel
    .fromPath(otudata)
    .ifEmpty {exit 1, "Otu files not found"}
    .map { tuple(it.baseName, it) }
    .set { otudata_chnl }

process normalize_otu_table {
    tag "$id"
    publishDir "${output_dir}/normalize_otu_table/${id}"

    input:
    set val(id), file(otu_file) from otudata_chnl

    output:
    set val(id), file("*.biom") into final_otu_chnl

    script:
    {{ normalize_otu_table }}
}
