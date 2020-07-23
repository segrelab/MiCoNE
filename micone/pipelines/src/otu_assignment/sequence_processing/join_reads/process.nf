#!/usr/bin/env nextflow

// Initialize variables
def sequence_16s = params.sequence_16s
def barcode = params.barcode
def output_dir = file(params.output_dir)


// Parameters
def min_overlap = params.min_overlap
def perc_max_diff = params.perc_max_diff


// Channels
Channel
    .fromFilePairs(sequence_16s)
    .ifEmpty { exit 1, "16S sequence reads not found" }
    .set { chnl_sequences }

Channel
    .fromPath(barcode)
    .ifEmpty { exit 1, "Barcode files not found" }
    .map { tuple(it.baseName.split('_barcodes')[0], it) }
    .set { chnl_barcodes }


// Processes

// Step0: Join sequence and barcode channels
chnl_sequences
    .join(chnl_barcodes)
    .set { chnl_sequence_join }

// Step1: Join reads
process  join_reads {
    tag "${id}"
    publishDir "${output_dir}/${id}", saveAs: { filename -> filename.split("/")[1] }, mode: 'copy', overwrite: true
    input:
    set val(id), val(sequence_files), file(barcode_file) from chnl_sequence_join
    output:
    set val(id), file('joined_reads/*_reads.fastq.gz'), file('joined_reads/*_barcodes.fastq.gz') into chnl_joined_reads
    script:
    {{ join_reads }}
}
