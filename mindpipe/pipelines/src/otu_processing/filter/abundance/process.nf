#!/usr/bin/env nextflow

// Initialize variables
def output_dir = file(params.output_dir)
def otu_table = params.otu_table


// Parameters
def count_thres = params.count_thres
def prevalence_thres = params.prevalence_thres
def abundance_thres = params.abundance_thres


// Channels
Channel
    .fromPath(otu_table)
    .ifEmpty { exit 1, "Otu files not found" }
    .map { tuple(it.getParent().baseName,  it) }
    .set { chnl_otudata }


// Processes
process filter {
    tag "${id}"
    publishDir "${output_dir}/${id}", saveAs: { filename -> filename.replaceAll("_filtered", "") }, mode: 'copy', overwrite: true
    input:
    set val(id), file(otu_file) from chnl_otudata
    output:
    set val(id), file("*_filtered.biom") into chnl_output
    script:
    {{ filter }}
}
