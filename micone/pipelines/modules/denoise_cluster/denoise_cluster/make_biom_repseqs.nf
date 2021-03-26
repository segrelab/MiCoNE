// Step2: Make representative sequences and biom table
process make_biom_repseqs {
    label 'dada2'
    tag "${id}"
    input:
        tuple val(id), file(seq_table_file)
    output:
        tuple val(id), file('*.biom'), file('*.fasta')
    script:
        template 'denoise_cluster/denoise_cluster/make_biom_repseqs.py'
}
