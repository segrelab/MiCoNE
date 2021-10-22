include { getHierarchy } from '../../../functions/functions.nf'

// Identify positions on the front and the tail that need to be trimmed based on
// a. quality and b. sequence retainment
process quality_analysis_single {
    label 'qiime2'
    tag "${meta.id}-${meta.run}"
    publishDir "${params.output_dir}/${f[0]}/${f[1]}/${f[2]}/${meta.id}-${meta.run}",
        mode: 'copy',
        overwrite: true
    input:
        tuple val(meta), file(qual_summary)
    output:
        tuple val(meta), file('trim.txt')
    script:
        String task_process = "${task.process}"
        f = getHierarchy(task_process)
        template 'sequence_processing/trimming/quality_analysis_single.py'
}

