#!/usr/bin/env nextflow

// Initialize variables
def sequence_reads = params.sequence_reads
def barcode_files = params.barcode_files
def mapping_files = params.mapping_files
def output_dir = file(params.output_dir)

// NOTE: All the above file muset have the same baseNames

// Parameters
def phred_quality_threshold = params.phred_quality_threshold

// Channels
Channel
    .fromPath(sequence_reads)
    .ifEmpty { exit 1, "16S sequence reads not found" }
    .map { tuple(it.baseName.split('_reads')[0], it) }
    .set { sequence_data_chnl }

Channel
    .fromPath(barcode_files)
    .ifEmpty { exit 1, "Barcode files not found" }
    .map { tuple(it.baseName.split('_barcodes')[0], it) }
    .set { barcode_data_chnl }

Channel
    .fromPath(mapping_files)
    .ifEmpty { exit 1, "Mapping data not found" }
    .map { tuple(it.baseName.split('_map')[0], it) }
    .into { mapping_validity_chnl; mapping_data_chnl }


// Processes

// Step0: Checking validity of the mapping file
process validate_mapping {
    tag "${id}"
    publishDir "${output_dir}/validation"

    input:
    set val(id), file(mapping_file) from mapping_validity_chnl

    output:
    file "${id}*" into validation_output
    stdout is_map_valid

    script:
    {{ validate_mapping }}
}

map_validity = (
    is_map_valid
    .map { e ->
        if (e == 'No errors or warnings were found in mapping file.\n')
           'No errors pipeline execution proceeding'
        else
            exit 1, 'Mapping file has errors'
    }
)


// Step1: Create lists of [id, sequence, barcode, mapping] for each sample
sequence_data_chnl
    .join(barcode_data_chnl)
    .join(mapping_data_chnl)
    .set { combined_data_chnl }

// Step2: Pass the above list of file-locations as comma-separated strings to `split_libraries_fastq.py`
process demultiplexing_fastq {
    tag "demultiplexing_illumina"
    publishDir "${output_dir}/demultiplexing_illumina"

    input:
    val(all_data) from combined_data_chnl.toList()

    output:
    file('*.fna') into demultiplexed_seqs

    script:
    combined_data = all_data
                    .inject(['', '', '']) {
            acc, x -> acc.withIndex().collect { e, i -> (e + ',' + x[i+1])}
        } .collect { it[1..-1] }
    (sequences, barcodes, mappings) = combined_data
    {{ demultiplexing_fastq }}
}
