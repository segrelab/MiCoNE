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
        joined_channel = trimming_paired_workflow.out.join(samplemetadata_channel, failOnMismatch: true)
    emit:
        // tuple val(meta), file('trimmed/*.fastq.gz'), file('trimmed/MANIFEST'), file(samplemetadata_files)
        joined_channel
}
