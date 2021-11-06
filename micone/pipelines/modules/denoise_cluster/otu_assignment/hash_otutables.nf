include { getHierarchy } from '../../../functions/functions.nf'

// Step3: Replace the ids with the hashes of the sequences
process hash_otutables {
    label 'qiime2'
    tag "${meta.id}"
    publishDir "${params.output_dir}/${f[0]}/${module_dir}/hashed_output/${meta.id}",
        mode: 'copy',
        overwrite: true
    input:
        val(meta)
        path(unhashed_otu_table)
        path(unhashed_rep_seqs)
        path(samplemetadata_files)
    output:
        tuple val(meta), file('otu_table.biom'), file('rep_seqs.fasta'), file('sample_metadata.tsv')
    script:
        String task_process = "${task.process}"
        f = getHierarchy(task_process)
        module_dir = "${meta.denoise_cluster}"
        template 'denoise_cluster/otu_assignment/hash_otutables.py'
}
