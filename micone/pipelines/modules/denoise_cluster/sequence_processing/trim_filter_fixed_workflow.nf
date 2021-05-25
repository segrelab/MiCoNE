include { import_sequences_py } from './import_sequences_py.nf'
include { export_visualization } from './export_visualization.nf'
include { quality_analysis } from './quality_analysis.nf'
include { trimming } from './trimming.nf'


workflow trim_filter_fixed_workflow {
    take:
        // tuple val(meta), file(sequence_file), file(manifest_file)
        input_channel
    main:
        input_channel \
            | import_sequences_py \
            | export_visualization \
            | quality_analysis \
            | join(input_channel) \
            | trimming
    emit:
        // triming and quality_analysis have publishDir
        // tuple val(meta), file('trimmed/*.fastq.gz'), file('trimmed/MANIFEST')
        trimming.out
}
