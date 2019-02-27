#!/usr/bin/env nextflow

// Initialize variables
def otudata = params.otudata
def otu_bootstrap = params.otu_bootstrap
def output_dir = file(params.output_dir)


// Parameters
def iterations = params.iterations
def ncpus = params.ncpus


// Channels

Channel
    .fromPath(otudata)
    .ifEmpty {exit 1, "Otu files not found"}
    .map { tuple(
        (it.getParent().baseName + '_' + it.baseName),
        it.getParent().baseName,
        it.baseName.split("_otu")[0],
        it
    ) }
    .set { chnl_otudata }

Channel
    .fromPath(otu_bootstrap)
    .ifEmpty {exit 1, "Otu files not found"}
    .map { tuple(
        (it.getParent().getParent().baseName + '_' + it.getParent().baseName + '_' + it.baseName),
        it.getParent().getParent().baseName,
        it.getParent().baseName,
        it
    ) }
    .set { chnl_otudata_boot }


// Processes

process sparcc_otu {
    tag "${id}"
    publishDir "${output_dir}/${dataset}"
    input:
    set val(id), val(dataset), val(level), file(otu_file) from chnl_otudata
    output:
    set val(id), file('*_corr.tsv') into chnl_corr
    script:
    {{ sparcc }}
}

process sparcc_boot {
    tag "${id}"
    publishDir "${output_dir}/${dataset}/${level}"
    input:
    set val(id), val(dataset), val(level), file(otu_file) from chnl_otudata_boot
    output:
    set val(id), file('*_corr.boot') into chnl_corr_boot
    script:
    {{ sparcc_boot }}
}
