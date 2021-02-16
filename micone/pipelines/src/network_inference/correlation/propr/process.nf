#!/usr/bin/env nextflow

// Initialize variables
def otudata = params.otudata
def otu_bootstrap = params.otu_bootstrap
def output_dir = file(params.output_dir)


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

process propr_otu {
    tag "${id}"
    publishDir "${output_dir}/${dataset}", mode: 'copy', overwrite: true
    input:
    set val(id), val(dataset), val(level), file(otu_file) from chnl_otudata
    output:
    set val(id), file('*_corr.tsv') into chnl_corr
    script:
    {{ propr }}
}

process propr_boot {
    tag "${id}"
    publishDir "${output_dir}/${dataset}/${level}", saveAs: { fname -> fname.split('.tsv')[0] + '.boot' }, mode: 'copy', overwrite: true
    input:
    set val(id), val(dataset), val(level), file(otu_file) from chnl_otudata_boot
    output:
    set val(id), file('*_corr.tsv') into chnl_corr_boot
    script:
    {{ propr }}
}
