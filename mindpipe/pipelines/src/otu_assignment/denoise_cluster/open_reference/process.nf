#!/usr/bin/env nextflow

// Initialize variables
def sequences = params.sequences
def sequence_reference = file(params.sequence_reference)
def output_dir = file(params.output_dir)


// Parameters
def parameters = file(params.parameters) // "-p $parameters"
def picking_method = params.picking_method // "-m $picking_method"
def ncpus = params.ncpus // "-a -O $ncpus"


// Channels
Channel
    .fromPath(sequences)
    .ifEmpty { exit 1, "16S sequences not found" }
    .set { chnl_sequences }

// Processes
process pick_open_reference_otus {
    tag "${sequence_file.baseName}"
    publishDir "${output_dir}/openref_picking"

    input:
    file sequence_files from chnl_sequences

    output:
    set file('otu_table.biom'), file('rep_seqs.fasta'), file('log*.txt') into output_chnl

    script:
    {{ pick_open_reference_otus }}
}
