include { getHierarchy } from '../../../functions/functions.nf'

// Step3: Replace the ids with hashes of the sequences
process hash_seqtables {
    label 'dada2'
    tag "${meta.id}"
    publishDir "${params.output_dir}/${f[0]}/${module_dir}/${directory}/${meta.id}",
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
        module_dir = f[1] == 'remove_bimera' ? 'remove_bimera' : "${meta.denoise_cluster}"
        directory = f[1] == 'remove_bimera' ? "filtered_output/${meta.denoise_cluster}" : 'hashed_output'
        template 'denoise_cluster/otu_assignment/hash_seqtables.py'
}
