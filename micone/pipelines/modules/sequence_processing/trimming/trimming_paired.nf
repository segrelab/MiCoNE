include { getHierarchy } from '../../../functions/functions.nf'

// Trimming the sequences using cutadapt
process trimming_paired {
    label 'qiime2'
    tag "${meta.id}-${meta.run}"
    publishDir "${params.output_dir}/${f[0]}/${f[1]}/trimmed_sequences/${meta.id}-${meta.run}",
        saveAs: { filename -> filename.split("/")[-1] },
        mode: 'copy',
        overwrite: true
    input:
        tuple val(meta), file(trim_cmd), file(sequence_files), file(manifest_file), file(sequence_metadata)
    output:
        tuple val(meta), file('trimmed/*.fastq.gz'), file('trimmed/MANIFEST'), file(sequence_metadata)
    script:
        String task_process = "${task.process}"
        f = getHierarchy(task_process)
        ncpus = params.sequence_processing.trimming['trimming_paired']['ncpus']
        max_ee = params.sequence_processing.trimming['trimming_paired']['max_ee']
        trunc_q = params.sequence_processing.trimming['trimming_paired']['trunc_q']
        template 'sequence_processing/trimming/trimming_paired.R'
}
