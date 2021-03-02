#!/usr/bin/env nextflow

// Initialize variables
def otudata = params.otudata
def sample_metadata = file(params.sample_metadata)
def output_dir = file(params.output_dir)

// Parameters
def ncpus = params.ncpus
def sensitive = params.sensitive
def heterogeneous = params.heterogeneous
def fdr_correction = params.fdr_correction


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

process flashweave_graph {
    tag "${id}"
    input:
    set val(id), val(dataset), val(level), file(otu_file) from chnl_otudata
    output:
    set val(id), file(otu_file), file('*_network.gml') into chnl_graph
    script:
    {{ flashweave }}
}

process flashweave_corr {
    tag "${id}"
    publishDir "${output_dir}/${dataset}", mode: 'copy', overwrite: true
    input:
    set val(id), file(otu_file), file(network_file) from chnl_graph
    output:
    set val(id), file('*_corr.tsv') into chnl_corr
    script:
    {{ export_gml }}
}
