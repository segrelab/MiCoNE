// 2. Obtain sampled quality profiles via demux viz
process export_visualization_single {
    label 'qiime2'
    tag "${meta.id}-${meta.run}"
    input:
        tuple val(meta), file(sequence_artifact)
    output:
        tuple val(meta), file('output/forward-seven-number-summaries.tsv')
    script:
        seq_samplesize = params.sequence_processing.trimming['export_visualization_single']['seq_samplesize']
        template 'sequence_processing/trimming/export_visualization.py'
}

