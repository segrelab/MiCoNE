// Import files
process import_reads {
    label 'qiime2'
    tag "${meta.id}"
    input:
        tuple val(meta), val(otu_table_file), file(rep_seqs), file(sample_metadata_file)
    output:
        tuple val(meta), val(otu_table_file), file('rep_seqs.qza'), file(sample_metadata_file)
    script:
        template 'tax_assignment/assign/import_reads.sh'
}
