// Step1a: Import files
process import_reads {
    tag "${id}"
    input:
    tuple val(id), file(rep_seqs)
    output:
    tuple val(id), file('rep_seqs.qza')
    script:
    template 'tax_assignment/assign/import_reads.sh'
}

