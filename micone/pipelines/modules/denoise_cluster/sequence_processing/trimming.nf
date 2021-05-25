include { getHierarchy } from '../../../functions/functions.nf'

// Trimming the sequences using cutadapt
process trimming {
    label 'qiime2'
    tag "${meta.id}"
    publishDir "${params.output_dir}/${f[0]}/${f[1]}/${f[2]}/${meta.id}",
        saveAs: { filename -> filename.split("/")[1] },
        mode: 'copy',
        overwrite: true
    input:
        tuple val(meta), file(trim_cmd), file(sequence_files), file(manifest_file)
    output:
        tuple val(meta), file('trimmed/*.fastq.gz'), file('trimmed/MANIFEST')
    script:
        String task_process = "${task.process}"
        f = getHierarchy(task_process)
        ncpus = params.denoise_cluster.sequence_processing['trimming']['ncpus']
        max_ee = params.denoise_cluster.sequence_processing['trimming']['max_ee']
        trunc_q = params.denoise_cluster.sequence_processing['trimming']['trunc_q']
        template 'denoise_cluster/sequence_processing/trimming.R'
}
