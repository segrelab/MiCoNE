// TODO: Move this to workflows
chnl_rep_seqs
    .combine(chnl_classifier_artifact)
    .tuple { chnl_repseqs_classifier }

// Step2: Assign taxonomy using the classifier
process assign_taxonomy {
    tag "${id}"
    publishDir "${output_dir}/${id}", mode: 'copy', overwrite: true
    input:
    tuple val(id), file(rep_seqs), file(classifier)
    output:
    tuple val(id), file('taxonomy.tsv')
    script:
    template 'tax_assignment/assign/assign_taxonomy_naivebayes.sh'
}
