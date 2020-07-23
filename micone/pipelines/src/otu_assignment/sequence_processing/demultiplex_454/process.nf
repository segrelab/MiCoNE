#!/usr/bin/env nextflow

// Initialize variables
def sequence_reads = params.sequence_reads
def quality_files = params.quality_files
def mapping_files = params.mapping_files  // NOTE: This has to be a single file
def output_dir = file(params.output_dir)


// Parameters
def qual_score_window = params.qual_score_window


// Channels
Channel
    .fromPath(sequence_reads)
    .ifEmpty { exit 1, "16S sequence reads not found" }
    .map { tuple(it.baseName.split('_reads')[0], it) }
    .set { sequence_data_chnl }

Channel
    .fromPath(quality_files)
    .ifEmpty { exit 1, "Sequence quality data not found" }
    .map { tuple(it.baseName.split('_qual')[0], it) }
    .set { quality_data_chnl }

Channel
    .fromPath(mapping_files)
    .ifEmpty { exit 1, "Mapping data not found" }
    .into { mapping_validity_chnl; mapping_data_chnl }


// Processes

// Step0: Checking validity of the mapping file
process validate_mapping {
    tag "$id"
    publishDir "${output_dir}", mode: 'copy', overwrite: true

    input:
    file(mapping_file) from mapping_validity_chnl

    output:
    file "*" into validation_output
    stdout is_map_valid

    script:
    {{ validate_mapping }}
}

map_validity = is_map_valid
                .map { e ->
                    if (e == 'No errors or warnings were found in mapping file.\n')
                       'No errors pipeline execution proceeding'
                    else
                        exit 1, 'Mapping file has errors'
                }

// Step1: Create lists of [id, sequence, quality] for each sample
sequence_data_chnl
    .join(quality_data_chnl)
    .set { combined_data_chnl }

// Step2: Pass the above list of file-locations as comma-separated strings to `split_libraries.py`
process demultiplexing_fasta {
    tag "demultiplexing_454"
    publishDir "${output_dir}", mode: 'copy', overwrite: true

    input:
    val(all_data) from combined_data_chnl.toList()
    file(mapping) from mapping_data_chnl

    output:
    file('*.fna') into demultiplexed_seqs

    script:
    combined_data = all_data
                    .inject(['', '']) {
            acc, x -> acc.withIndex().collect { e, i -> (e + ',' + x[i+1])}
        } .collect { it[1..-1] }
    (sequences, qualities) = combined_data
    {{ demultiplexing_fasta }}
}
