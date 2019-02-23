#!/usr/bin/env nextflow

// Initialize variables
def otudata = params.otudata
def output_dir = file(params.output_dir)


// Parameters
def iterations = params.iterations


// Channels

Channel
    .fromPath(otudata)
    .ifEmpty {exit 1, "Otu files not found"}
    .map { tuple(
        (it.getParent().getParent().baseName + '_' + it.getParent().baseName + '_' + it.baseName),
        it.getParent().getParent().baseName,
        it.getParent().baseName,
        it
    ) }
    .set { chnl_otudata_tsv }


// Processes

process sparcc {
    tag "${id}"
    publishDir "${output_dir}/${dataset}/${level}"
    input:
    set val(id), val(dataset), val(level), file(otu_file) from chnl_otudata_tsv
    output:
    set val(id), file('*_corr.tsv') into chnl_corr
    script:
    {{ sparcc }}
}
