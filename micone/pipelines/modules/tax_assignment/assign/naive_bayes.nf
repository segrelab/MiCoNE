// Assign taxonomy using the naive bayes classifier
process naive_bayes {
    label 'qiime2'
    tag "${meta.id}"
    input:
        tuple val(meta), file(otu_table), file(rep_seqs), file(sample_metadata)
    output:
        tuple val(meta), file(otu_table), file('taxonomy.tsv'), file(sample_metadata)
    script:
        meta.tax_assignment = "naive_bayes"
        classifier = params.tax_assignment.assign['naive_bayes']['classifier']
        confidence = params.tax_assignment.assign['naive_bayes']['confidence']
        ncpus = params.tax_assignment.assign['naive_bayes']['ncpus']
        template 'tax_assignment/assign/assign_taxonomy_naivebayes.sh'
}
