#!/usr/bin/env nextflow

def output_dir = file(params.output_dir)
def otu_table = params.otu_table

def tax_levels = params.tax_levels

Channel
    .fromPath(otu_table)
    .ifEmpty {exit 1, "Otu files not found"}
    .map { tuple(it.getParent().baseName, it) }
    .set { chnl_otudata }

process group {
    tag "$id"
    publishDir "${output_dir}/${id}", mode: 'copy', overwrite: true
    input:
    set val(id), file(otu_file) from chnl_otudata
    output:
    set val(id), file("*.biom") into final_otu_chnl
    set val(id), file("*.json") into final_childrendata_chnl
    script:
    {{ group }}
}
