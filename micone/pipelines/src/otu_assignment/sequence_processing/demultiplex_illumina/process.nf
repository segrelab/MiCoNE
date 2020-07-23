#!/usr/bin/env nextflow

// Initialize variables
def sequence_16s = params.sequence_16s
def barcode = params.barcode
def sample_barcode_mapping = params.sample_barcode_mapping
def output_dir = file(params.output_dir)

// NOTE: All the above file muset have the same baseNames

// Parameters
def rev_comp_barcodes = params.rev_comp_barcodes
def rev_comp_mapping_barcodes = params.rev_comp_mapping_barcodes


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
    .set { chnl_sequence_import }

// Step2: Import the sequences into a qiime2 artifact
process import_sequences {
    tag "${id}"
    input:
    set val(id), file(sequence_file), file(barcode_file) from chnl_sequence_import
    output:
    set val(id), file('*_sequences.qza') into chnl_seqartifact
    script:
    {{ import_sequences }}
}

chnl_seqartifact
    .join(chnl_mapping)
    .set { chnl_demux_input }


// Step3: demultiplex
process demultiplex {
    tag "${id}"
    input:
    set val(id), file(sequence_artifact), file(mapping_file) from chnl_demux_input
    output:
    set val(id), file('*_demux.qza') into chnl_seqdemux_export
    script:
    def rcb = rev_comp_barcodes == 'True' ? '--p-rev-comp-barcodes' : '--p-no-rev-comp-barcodes'
    def rcmb = rev_comp_mapping_barcodes == 'True' ? '--p-rev-comp-mapping-barcodes' : '--p-no-rev-comp-mapping-barcodes'
    {{ demultiplex }}
}

// Step4: Export the sequences and fix the manifest file
process export_sequences {
    tag "${id}"
    publishDir "${output_dir}/${id}", saveAs: { filename -> filename.split("/")[1] }, mode: 'copy', overwrite: true
    input:
    set val(id), file(demux_artifact) from chnl_seqdemux_export
    output:
    set val(id), file('demux_seqs/*.fastq.gz'), file('demux_seqs/MANIFEST') into chnl_seqdemux
    script:
    {{ export_sequences }}
}
