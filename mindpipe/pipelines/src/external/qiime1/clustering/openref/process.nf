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
process pick_open_reference_otus {
    tag "${sequence_file.baseName}"
    publishDir "${output_dir}/openref_picking"

    input:
    set file(sequence_files) from sequence_data_chnl.collect()

    output:
    set file('otu_table.biom'), file('seqs_rep_set.fasta'), file('log*.txt') into output_chnl

    script:
    {{ pick_open_reference_otus }}
}
