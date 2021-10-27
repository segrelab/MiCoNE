include { import_sequences_single } from './import_sequences_single.nf'
include { export_visualization_single } from './export_visualization_single.nf'
include { quality_analysis_single } from './quality_analysis_single.nf'
include { trimming_single } from './trimming_single.nf'


workflow trimming_single_workflow {
    take:
        // tuple val(meta), file(sequence_files), file(manifest_file), file(sequence_metadata)
        input_channel
    main:
        input_channel \
            | import_sequences_single \
            | export_visualization_single \
            | quality_analysis_single \
            | join(input_channel) \
            | trimming_single
    emit:
        // triming and quality_analysis_single have publishDir
        // tuple val(meta), file('trimmed/*.fastq.gz'), file('trimmed/MANIFEST'), file(sequence_metadata)
        trimming_single.out
}
