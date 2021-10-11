include { demultiplexing_single_workflow } from './demultiplexing/demultiplexing_single_workflow.nf'
include { trimming_single_workflow } from './trimming/trimming_single_workflow.nf'


workflow sequence_processing_single_workflow {
    take:
        // tuple val(meta), file(sequence_file), file(barcode_file), file(mapping_file)
        input_channel
        // tuple val(meta), file(samplemetadata_files)
        samplemetadata_channel
    main:
        input_channel \
            | demultiplexing_single_workflow \
            | trimming_single_workflow
    emit:
        // tuple val(meta), file('trimmed/*.fastq.gz'), file('trimmed/MANIFEST')
        trimming_single_workflow.out
        // tuple val(meta), file(samplemetadata_files)
        samplemetadata_channel
}
