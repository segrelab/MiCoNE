include { updateMeta } from '../../../functions/functions.nf'

// Blast representative sequences against the blast database
process blast {
    label 'qiime2'
    tag "${new_meta.id}"
    input:
        tuple val(meta), file(otu_table_file), file(repseq_artifact), file(sample_metadata_file)
    when:
        'blast' in params.tax_assignment.assign['selection']
    output:
        tuple val(new_meta), file(otu_table_file), file("taxonomy.tsv"), file(sample_metadata_file)
    script:
        new_meta = updateMeta(meta)
        reference_sequences = params.tax_assignment.assign['blast']['reference_sequences']
        new_meta.tax_assignment = "blast(${file(reference_sequences).baseName.split('-')[0]})"
        new_meta.taxonomy_database = reference_sequences
        tax_map = params.tax_assignment.assign['blast']['tax_map']
        max_accepts = params.tax_assignment.assign['blast']['max_accepts']
        perc_identity = params.tax_assignment.assign['blast']['perc_identity']
        evalue = params.tax_assignment.assign['blast']['evalue']
        min_consensus = params.tax_assignment.assign['blast']['min_consensus']
        template 'tax_assignment/assign/assign_taxonomy_blast.sh'
}
