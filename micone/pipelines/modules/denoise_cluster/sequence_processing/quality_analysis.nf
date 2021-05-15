// Identify positions on the front and the tail that need to be trimmed based on
// a. quality and b. sequence retainment
process quality_analysis {
    label 'qiime2'
    tag "${id}"
    publishDir "${params.output_dir}/${task.process}/${id}/quality_summary", mode: 'copy', overwrite: true
    input:
        tuple val(id), file(qual_summary)
    output:
        tuple val(id), file('trim.txt')
    script:
        template 'denoise_cluster/sequence_processing/quality_analysis.py'
}

