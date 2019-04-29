#!/usr/bin/env nextflow

// Initialize variables
def otudata = params.otudata
def output_dir = file(params.output_dir)


// Parameters
def bootstraps = params.bootstraps
def ncpus = params.ncpus
def filter_flag = params.filter_flag


// Channels

Channel
    .fromPath(otudata)
    .ifEmpty {exit 1, "Otu files not found"}
    .map { tuple(
        (it.getParent().baseName + '_' + it.baseName.split("_otu")[0]),
        it.getParent().baseName,
        it.baseName.split("_otu")[0],
        it
    ) }
    .set { chnl_otudata_tsv }


// Processes

process resample {
    tag "${id}"
    input:
    set val(id), val(dataset), val(level), file(otu_file) from chnl_otudata_tsv
    output:
    set val(id), val(dataset), val(level), file('bootstraps/*.boot.temp') into chnl_otudata_bootstrap
    script:
    {{ resample }}
}

process filter {
    tag "${id}"
    publishDir "${output_dir}/${dataset}/${level}", saveAs: { filename -> filename.split("/")[-1] }, mode: 'copy', overwrite: true
    input:
    set val(id), val(dataset), val(level), file(boot_file) from chnl_otudata_bootstrap
    output:
    set val(id), val(dataset), val(level), file('filtered/*.boot') into chnl_bootstrap_filter
    script:
    {{ filter }}
}
