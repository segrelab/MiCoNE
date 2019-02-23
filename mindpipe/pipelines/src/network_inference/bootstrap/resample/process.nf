#!/usr/bin/env nextflow

// Initialize variables
def otudata = params.otudata
def output_dir = file(params.output_dir)


// Parameters
def bootstraps = params.bootstraps


// Channels

Channel
    .fromPath(otudata)
    .ifEmpty {exit 1, "Otu files not found"}
    .map { tuple(
        (it.getParent().baseName + '_' + it.baseName),
        it.getParent().baseName,
        it.baseName,
        it
    ) }
    .set { chnl_otudata_tsv }


// Processes

process resample {
    tag "${id}"
    publishDir "${output_dir}/${dataset}/${level}", saveAs: { filename -> filename.split("/")[-1] }
    input:
    set val(id), val(dataset), val(level), file(otu_file) from chnl_otudata_tsv
    output:
    set val(id), file('bootstraps/*.tsv') into chnl_otudata_bootstrap
    script:
    {{ resample }}
}
