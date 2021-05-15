// 2. Obtain sampled quality profiles via demux viz
process export_visualization {
    label 'qiime2'
    tag "${id}"
    input:
        tuple val(id), file(sequence_artifact)
    output:
        tuple val(id), file('output/forward-seven-number-summaries.csv')
    script:
        template 'denoise_cluster/sequence_processing/export_visualization.py'
}

