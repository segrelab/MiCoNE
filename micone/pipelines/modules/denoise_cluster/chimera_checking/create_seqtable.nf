// Step1: Create a sequence table
process create_seqtable {
    label 'dada2'
    tag "${id}"
    input:
        tuple val(id), file(otutable_file), file(repseqs_file)
    output:
        tuple val(id), file('seq_table.tsv')
    script:
        template 'denoise_cluster/chimera_checking/create_seqtable.py'
}
