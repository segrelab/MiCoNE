// Step3: Replace the ids with hashes of the sequences
process hashing3 {
    label 'dada2'
    tag "${id}"
    publishDir "${params.output_dir}/${id}", mode: 'copy', overwrite: true
    input:
        tuple val(id), file(unhashed_otu_table), file(unhashed_rep_seqs)
    output:
        tuple val(id), file('otu_table.biom'), file('rep_seqs.fasta')
    script:
        template 'denoise_cluster/denoise_cluster/hashing3.py'
}
