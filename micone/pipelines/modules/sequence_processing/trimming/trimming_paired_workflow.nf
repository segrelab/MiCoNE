include { import_sequences_paired } from './import_sequences_paired.nf'
include { export_visualization } from './export_visualization.nf'
include { quality_analysis_paired } from './quality_analysis_paired.nf'
include { trimming_paired } from './trimming_paired.nf'


workflow trimming_paired_workflow {
    take:
        // tuple val(meta), file(sequence_file), file(manifest_file)
        input_channel
    main:
        input_channel \
            | import_sequences_paired \
            | export_visualization \
            | quality_analysis_paired \
            | join(input_channel) \
            | trimming_paired
    emit:
        // triming and quality_analysis_paired have publishDir
        // tuple val(meta), file('trimmed/*.fastq.gz'), file('trimmed/MANIFEST')
        trimming_paired.out
}
