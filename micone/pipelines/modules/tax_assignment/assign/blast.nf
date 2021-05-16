// Blast representative sequences against the blast database
process blast {
    label 'qiime2'
    tag "${meta.id}"
    input:
        tuple val(meta), file(otu_table_file), file(repseq_artifact), file(sample_metadata_file)
    when:
        'blast' in params.tax_assignment.assign['selection']
    output:
        tuple val(meta), file(otu_table_file), file("taxonomy.tsv"), file(sample_metadata_file)
    script:
        meta.tax_assignment = "blast"
        reference_sequences = params.tax_assignment.assign['blast']['reference_sequences']
        tax_map = params.tax_assignment.assign['blast']['tax_map']
        max_accepts = params.tax_assignment.assign['blast']['max_accepts']
        perc_identity = params.tax_assignment.assign['blast']['perc_identity']
        evalue = params.tax_assignment.assign['blast']['evalue']
        min_consensus = params.tax_assignment.assign['blast']['min_consensus']
        template 'tax_assignment/assign/assign_taxonomy_blast.sh'
}
