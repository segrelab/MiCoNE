#!/usr/bin/env nextflow

// Initialize variables
def input_folder = params.input_folder
def output_dir = file(params.output_dir)


// Parameters
def input_type = params.input_type


// Channels
Channel
    .fromPath(input_folder)
    .ifEmpty { exit 1, "Input folder not found" }
    .set { chnl_input_folder }


// Processes
process sequence_importer {
    tag "sequence"
    publishDir "${output_dir}/importer"

    input:
    file sequence_folder from chnl_input_folder

    output:
    file('*.qza') into output_chnl

    script:
    {{ sequence_importer }}
}
