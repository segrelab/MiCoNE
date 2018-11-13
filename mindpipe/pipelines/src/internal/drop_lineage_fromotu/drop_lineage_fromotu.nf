#!/usr/bin/env nextflow

def output_dir = file(params.output_dir)
def otudata = params.otudata


// TODO: Modify this to actually take in sample metadata
Channel
    .fromPath(otudata)
    .ifEmpty {exit 1, "Otu files not found"}
    .map {
        tuple(
            it.getParent().toString().split("/")[-1],
            it
        )
    }
    .set { otu_chnl }

process drop_lineage {
    tag "$id"
    publishDir "${output_dir}/drop_lineage"

    input:
    set val(id), file(otu_file) from otu_chnl

    output:
    set val(id), file("*_otu.tsv") into new_otu_table
    set val(id), file("*_lineage.txt") into lineage_data_raw
    set val(id), file("*_obs.txt") into observations_raw

    script:
    {{ drop_lineage }}
}

process make_lineage {
    tag "$id"
    publishDir "${output_dir}/make_lineage"

    input:
    set val(id), file(lineage_file) from lineage_data_raw

    output:
    set val(id), file("*_taxondata.csv") into lineage_data_parsed

    script:
    {{ make_lineage }}
}

process make_sample_metadata {
    tag "$id"
    publishDir "${output_dir}/make_sample_metadata"

    input:
    set val(id), file(obs_file) from observations_raw

    output:
    set val(id), file("*_sample_metadata.csv") into observations_parsed

    script:
    {{ make_sample_metadata }}
}