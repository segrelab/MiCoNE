// 2. Obtain sampled quality profiles via demux viz
process export_visualization {
    tag "${id}"
    publishDir "${output_dir}/${id}/quality_summary", saveAs: { filename -> filename.split("/")[1] }, mode: 'copy', overwrite: true
    input:
    tuple val(id), file(sequence_artifact)
    output:
    tuple val(id), file('output/forward-seven-number-summaries.csv')
    script:
    template 'denoise_cluster/sequence_processing/export_visualization.py'
}

