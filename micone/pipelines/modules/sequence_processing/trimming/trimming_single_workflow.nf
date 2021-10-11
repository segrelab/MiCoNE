include { import_sequences_single } from './import_sequences_single.nf'
include { export_visualization } from './export_visualization.nf'
include { quality_analysis_single } from './quality_analysis_single.nf'
include { trimming_single } from './trimming_single.nf'


workflow trimming_single_workflow {
    take:
        // tuple val(meta), file(sequence_file), file(manifest_file)
        input_channel
    main:
        input_channel \
            | import_sequences_single \
            | export_visualization \
            | quality_analysis_single \
            | join(input_channel) \
            | trimming_single
    emit:
        // triming and quality_analysis_single have publishDir
        // tuple val(meta), file('trimmed/*.fastq.gz'), file('trimmed/MANIFEST')
        trimming_single.out
}
