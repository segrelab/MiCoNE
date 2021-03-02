#!/usr/bin/env nextflow

// Initialize variables
def otudata = params.otudata
def output_dir = file(params.output_dir)


// Parameters
def method = params.method
def ncpus = params.ncpus
def nreps = params.nreps
def nlambda = params.nlambda
def lambda_min_ratio = params.lambda_min_ratio


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


// Processes

process spieceasi_otu {
    tag "${id}"
    publishDir "${output_dir}/${dataset}", mode: 'copy', overwrite: true
    input:
    set val(id), val(dataset), val(level), file(otu_file) from chnl_otudata
    output:
    set val(id), file('*_corr.tsv') into chnl_corr
    script:
    {{ spieceasi }}
}
