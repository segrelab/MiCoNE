include { demultiplexing_paired_workflow } from './demultiplexing/demultiplexing_paired_workflow.nf'
include { trimming_paired_workflow } from './trimming/trimming_paired_workflow.nf'


workflow sequence_processing_paired_workflow {
    take:
        // tuple val(meta), file(sequence_file), file(barcode_file), file(mapping_file)
        input_channel
        // tuple val(meta), file(samplemetadata_files)
        samplemetadata_channel
    main:
        input_channel \
            | demultiplexing_paired_workflow \
            | trimming_paired_workflow
        tr_map_channel = trimming_paired_workflow.out.map {
            [it[0]["id"] + "-" + it[0]["run"], it[0], it[1], it[2], it[3]]
        }
        sm_map_channel = samplemetadata_channel.map { [it[0]["id"] + "-" + it[0]["run"], it[1]] }
        joined_map_channel = tr_map_channel.join(sm_map_channel, by: 0, failOnMismatch: true)
        joined_channel = joined_map_channel.map { [it[1], it[2], it[3], it[4], it[5]] }
    emit:
    // tuple val(meta), file('trimmed/*.fastq.gz'), file('trimmed/MANIFEST'), file(sequence_metadata), file(samplemetadata_files)
        joined_channel
}
