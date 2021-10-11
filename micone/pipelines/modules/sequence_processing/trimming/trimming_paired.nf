include { getHierarchy } from '../../../functions/functions.nf'

// Trimming the sequences using cutadapt
process trimming_paired {
    label 'qiime2'
    tag "${meta.id}"
    publishDir "${params.output_dir}/${f[0]}/${f[1]}/trimmed_sequences/${meta.id}",
        saveAs: { filename -> filename.split("/")[1] },
        mode: 'copy',
        overwrite: true
    input:
        tuple val(meta), file(trim_cmds), file(sequence_files), file(manifest_file)
    output:
        tuple val(meta), file('trimmed/*.fastq.gz'), file('trimmed/MANIFEST')
    script:
        String task_process = "${task.process}"
        f = getHierarchy(task_process)
        ncpus = params.sequence_processing.trimming['trimming_paired']['ncpus']
        max_ee = params.sequence_processing.trimming['trimming_paired']['max_ee']
        trunc_q = params.sequence_processing.trimming['trimming_paired']['trunc_q']
        template 'sequence_processing/trimming/trimming_paired.R'
}
