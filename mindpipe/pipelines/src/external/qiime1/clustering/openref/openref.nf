#!/usr/bin/env nextflow

// Initialize variables
def sequences = params.sequences
def references = file(params.references)
def output_dir = file(params.output_dir)


// Parameters
def parameters = file(params.parameters) // "-p $parameters"
def picking_method = params.picking_method // "-m $picking_method"
def ncpus = params.ncpus // "-a -O $ncpus"
def percent_subsample = params.percent_subsample // "-s $percent_subsample"


// Channels
Channel
    .fromPath(sequences)
    .ifEmpty { exit 1, "16S sequences not found" }
    .set { sequence_data_chnl }

// Processes

// Step1: Pick open reference otus
process pick_open_reference_otus {
    tag "open_reference"
    publishDir "${output_dir}/openref_picking"

    input:
    val sequence_files from sequence_data_chnl.collect()

    output:
    set file('*.biom'),
        file('rep_set.{fna,fasta}'),
        file('rep_set.tre'),
        file('log*.txt') into output_chnl

    script:
    sequence_list = sequence_files.join(',')
    {{ pick_open_reference_otus }}
}