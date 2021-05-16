// Step1: Create a sequence table
process create_seqtable {
    label 'dada2'
    tag "${meta.id}"
    input:
        tuple val(meta), file(otutable_file), file(repseqs_file)
    output:
        tuple val(meta), file('seq_table.tsv')
    script:
        template 'denoise_cluster/chimera_checking/create_seqtable.py'
}
