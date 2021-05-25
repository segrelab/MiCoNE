include { getHierarchy } from '../../../functions/functions.nf'

// Identify positions on the front and the tail that need to be trimmed based on
// a. quality and b. sequence retainment
process quality_analysis {
    label 'qiime2'
    tag "${meta.id}"
    publishDir "${params.output_dir}/${f[0]}/${f[1]}/${f[2]}/${meta.id}",
        mode: 'copy',
        overwrite: true
    input:
        tuple val(meta), file(qual_summary)
    output:
        tuple val(meta), file('trim.txt')
    script:
        String task_process = "${task.process}"
        f = getHierarchy(task_process)
        template 'denoise_cluster/sequence_processing/quality_analysis.py'
}

