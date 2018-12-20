#!/usr/bin/env nextflow

// Initialize variables
def sequences = params.sequences
def sequence_reference = file(params.sequence_reference)
def taxonomy_mapping = file(params.taxonomy_mapping)
def output_dir = file(params.output_dir)


// Parameters
def parameters = file(params.parameters)
def ncpus = params.ncpus // "-a -O $ncpus"


// Channels
Channel
    .fromPath(sequences)
    .ifEmpty { exit 1, "16S sequence fasta files not found" }
    .set { chnl_sequences }


// Processes
process pick_closed_reference_otus {
    tag "${sequence_file.baseName}"
    publishDir "${output_dir}/closedref_picking"

    input:
    val sequence_file from chnl_sequences

    output:
    set file('otu_table.biom'), file('rep_set/seqs_rep_set.fasta') file('log*.txt') into output_chnl

    script:
    {{ pick_closed_reference_otus }}
}
