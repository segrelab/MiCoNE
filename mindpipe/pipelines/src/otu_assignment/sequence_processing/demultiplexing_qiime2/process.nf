#!/usr/bin/env nextflow

// Initialize variables
def sequence_artifacts = params.sequence_artifacts
def barcodes_file = file(params.barcodes_file)
def output_dir = file(params.output_dir)


// Parameters
def barcodes_column = params.barcodes_column
def rev_comp_barcodes = params.rev_comp_barcodes
def rev_comp_mapping_barcodes = params.rev_comp_mapping_barcodes


// Channels
Channel
    .fromPath(sequence_artifacts)
    .ifEmpty { exit 1, "Sequence artifacts not found" }
    .into { sequence_artifact_filetype; sequence_artifact_demultiplexing }


// Processes
process get_filetype {
    tag "filetype"
    publishDir "${output_dir}/filetype"

    input:
    file sequence_artifact from sequence_artifact_filetype

    output:
    file ('filetype.txt') into sequence_type_chnl

    script:
    {{ get_filetype }}
}

// TODO: Error handling if filetype is not 'q2_demux._format.*'
process demultiplexing {
    tag "demultiplexing"
    publishDir "${output_dir}/demultiplexing"
    echo true

    input:
    file sequence_artifact from sequence_artifact_demultiplexing
    val filetype from sequence_type_chnl

    output:
    file('*.qza') into output_chnl

    script:
    def itype = filetype.text.contains('EMPSingleEnd') ? 'single' : 'paired'
    def fname = sequence_artifact.baseName.split('_sequences')[0]
    def rcb = rev_comp_barcodes == 'True' ? '--p-rev-comp-barcodes' : '--p-no-rev-comp-barcodes'
    def rcmb = rev_comp_mapping_barcodes == 'True' ? '--p-rev-comp-mapping-barcodes' : '--p-no-rev-comp-mapping-barcodes'
    {{ demultiplexing }}
}