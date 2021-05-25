include { getHierarchy } from '../../../functions/functions.nf'

// Step3: Replace the ids with hashes of the sequences
process hashing3 {
    label 'dada2'
    tag "${meta.id}"
    publishDir "${params.output_dir}/${f[0]}/${f[1]}/${f[2]}/${meta.id}",
        mode: 'copy',
        overwrite: true
    input:
        tuple val(meta), file(unhashed_otu_table), file(unhashed_rep_seqs)
    output:
        tuple val(meta), file('otu_table.biom'), file('rep_seqs.fasta')
    script:
        String task_process = "${task.process}"
        f = getHierarchy(task_process)
        template 'denoise_cluster/denoise_cluster/hashing3.py'
}
