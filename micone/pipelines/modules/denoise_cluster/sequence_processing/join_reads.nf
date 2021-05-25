include { getHierarchy } from '../../../functions/functions.nf'

// Join reads
process join_reads {
    label 'qiime2'
    tag "${meta.id}"
    publishDir "${params.output_dir}/${f[0]}/${f[1]}/${f[2]}/${meta.id}",
        mode: 'copy',
        overwrite: true
    input:
        tuple val(meta), file(demux_artifact)
    output:
        tuple val(meta), file('*_joined.qza')
    script:
        String task_process = "${task.process}"
        f = getHierarchy(task_process)
        template 'denoise_cluster/sequence_processing/join_reads.sh'
}
