// TODO: Implement both fixed length and variable length (based on quality) trimming

// Processes
process get_visualization {
    tag "visualization"
    publishDir "${output_dir}", mode: 'copy', overwrite: true

    input:
    file sequence_artifact from sequence_artifact_viz

    output:
    file ('output/*-seven-number-summaries.csv') into sequence_viz_chnl

    script:
    {{ get_visualization }}
}

process quality_analysis {
    tag "quality_analysis"
    publishDir "${output_dir}", mode: 'copy', overwrite: true

    input:
    val filetype from filetype_quality
    file summaries from sequence_viz_chnl

    output:
    file ('trim.txt') into quality_cmd_chnl

    script:
    def reverse = itype == 'paired' ? "reverse-seven-number-summaries.csv" : ""
    {{ quality_analysis }}
}
