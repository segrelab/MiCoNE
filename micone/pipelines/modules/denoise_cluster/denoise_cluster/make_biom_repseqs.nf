// Step2: Make representative sequences and biom table
process make_biom_repseqs {
    tag "${id}"
    publishDir "${output_dir}/${id}", mode: 'copy', overwrite: true
    input:
    tuple val(id), file(seq_table_file)
    output:
    tuple val(id), file('*.biom'), file('*.fasta')
    script:
    template 'denoise_cluster/denoise_cluster/make_biom_repseqs.py'
}
