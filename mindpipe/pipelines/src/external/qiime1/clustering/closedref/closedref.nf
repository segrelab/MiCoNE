#!/usr/bin/env nextflow

// Initialize variables
def sequences = params.sequences
def references = file(params.references)
def taxonomy = file(params.taxonomy)
def output_dir = file(params.output_dir)


// Parameters
def parameters = file(params.parameters)
def ncpus = params.ncpus // "-a -O $ncpus"


// Channels
Channel
    .fromPath(sequences)
    .ifEmpty { exit 1, "16S sequences not found" }
    .set { sequence_data_chnl }


// Processes

// Step1: Pick closed reference otus
process pick_closed_reference_otus {
    tag "closed_reference"
    publishDir "${output_dir}/closedref_picking"

    input:
    val sequence_files from sequence_data_chnl.collect()

    output:
    set file('otu_table.biom'),
        file('*.tre'),
        file('log*.txt') into output_chnl

    script:
    sequence_list = sequence_files.join(',')
    {{ pick_closed_reference_otus }}
}