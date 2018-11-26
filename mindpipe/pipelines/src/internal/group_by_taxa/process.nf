#!/usr/bin/env nextflow

def output_dir = file(params.output_dir)
def otudata = params.otudata
def sample_metadata = params.sample_metadata
def lineagedata = params.lineagedata

def rm_sparse_otu = params.rm_sparse_otu
def rm_sparse_samples = params.rm_sparse_samples
def tax_levels = params.tax_levels

Channel
    .fromPath(otudata)
    .ifEmpty {exit 1, "Otu files not found"}
    .map { tuple(it.baseName, it) }
    .set { otudata_chnl }

process group_by_taxa {
    tag "$id"
    publishDir "${output_dir}/group_by_taxa/${id}"

    input:
    set val(id), file(otu_file) from otudata_chnl

    output:
    set val(id), file("*.biom") into final_otu_chnl
    set val(id), file("*.json") into final_childrendata_chnl

    script:
    {{ group_by_taxa }}
}
