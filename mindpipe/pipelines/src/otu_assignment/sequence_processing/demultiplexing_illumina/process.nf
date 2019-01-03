#!/usr/bin/env nextflow

// Initialize variables
def sequence_16s = params.sequence_16s
def barcode = params.barcode
def sample_barcode_mapping = params.sample_barcode_mapping
def output_dir = file(params.output_dir)

// NOTE: All the above file muset have the same baseNames


// Channels
Channel
    .fromPath(sequence_16s)
    .ifEmpty { exit 1, "16S sequence reads not found" }
    .map { tuple(it.baseName.split('_reads')[0], it) }
    .set { chnl_sequences }

Channel
    .fromPath(barcode)
    .ifEmpty { exit 1, "Barcode files not found" }
    .map { tuple(it.baseName.split('_barcodes')[0], it) }
    .set { chnl_barcodes }

Channel
    .fromPath(sample_barcode_mapping)
    .ifEmpty { exit 1, "Mapping data not found" }
    .map { tuple(it.baseName.split('_map')[0], it) }
    .into { chnl_mapping }


// Processes

// Step1: Create lists of [id, sequence, barcode, mapping] for each sample
chnl_sequences
    .join(chnl_barcodes)
    .join(chnl_mapping)
    .set { chnl_combined_data }

// Step2: Demultiplexing
process demultiplexing {
    tag "${id}"
    publishDir "${output_dir}/demultiplexing"

    input:
    set val(id), file(sequence_file), file(barcode_file), file(mapping_file) from chnl_combined_data

    output:
    set file('demux_seqs/*.fastq.gz'), file('demux_seqs/MANIFEST') into demultiplexed_seqs

    script:
    {{ demultiplexing }}
}
