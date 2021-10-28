include { updateMeta } from '../../../functions/functions.nf'

// Assign taxonomy using the naive bayes classifier
process naive_bayes {
    label 'qiime2'
    tag "${new_meta.id}:${classifier_id}"
    input:
        tuple val(meta), file(otu_table), file(rep_seqs), file(sample_metadata)
        each classifier
    when:
        'naive_bayes' in params.tax_assignment.assign['selection']
    output:
        tuple val(new_meta), file(otu_table), file('taxonomy.tsv'), file(sample_metadata)
    script:
        new_meta = updateMeta(meta)
        classifier_id = "${file(classifier).simpleName}"
        new_meta.tax_assignment = "naive_bayes(${classifier_id})"
        new_meta.taxonomy_database = classifier
        confidence = params.tax_assignment.assign['naive_bayes']['confidence']
        ncpus = params.tax_assignment.assign['naive_bayes']['ncpus']
        template 'tax_assignment/assign/assign_taxonomy_naivebayes.sh'
}
