// Step3: Replace the ids with the hashes of the sequences
process hashing2 {
    label 'qiime1'
    tag "${id}"
    publishDir "${params.output_dir}/${task.process}/${id}", mode: 'copy', overwrite: true
    input:
        tuple val(id), file(unhashed_otu_table), file(unhashed_rep_seqs), file(log)
    output:
        tuple val(id), file('otu_table.biom'), file('rep_seqs.fasta')
    script:
        template 'denoise_cluster/denoise_cluster/hashing2.py'
}
