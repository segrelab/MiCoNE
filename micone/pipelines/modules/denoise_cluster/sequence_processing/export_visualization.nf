// 2. Obtain sampled quality profiles via demux viz
process export_visualization {
    label 'qiime2'
    tag "${meta.id}"
    input:
        tuple val(meta), file(sequence_artifact)
    output:
        tuple val(meta), file('output/forward-seven-number-summaries.tsv')
    script:
        seq_samplesize = params.denoise_cluster.sequence_processing['export_visualization']['seq_samplesize']
        template 'denoise_cluster/sequence_processing/export_visualization.py'
}

