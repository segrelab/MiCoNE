#!/usr/bin/env nextflow

def output_dir = file(params.output_dir)
def otudata = params.otudata


Channel
    .fromPath(otudata)
    .ifEmpty {exit 1, "Otu files not found"}
    .map { tuple(it.baseName, it) }
    .set { chnl_otu }

process biom2tsv {
    tag "$id"
    publishDir "${output_dir}/biom2tsv"

    input:
    set val(id), file(otu_file) from chnl_otu

    output:
    set val(id), file("*_otu.tsv") into new_otu_table
    set val(id), file("*_obs_metadata.csv") into lineage_data_raw
    set val(id), file("*_sample_metadata.tsv") into observations_raw

    script:
    {{ biom2tsv }}
}
