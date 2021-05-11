// Assign taxonomy using the naive bayes classifier
process naive_bayes {
    label 'qiime2'
    tag "${id}"
    input:
        tuple val(id), file(rep_seqs), file(classifier)
    output:
        tuple val(id), file('taxonomy.tsv')
    script:
        template 'tax_assignment/assign/assign_taxonomy_naivebayes.sh'
}
