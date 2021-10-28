include { naive_bayes } from './naive_bayes.nf'
include { add_md2biom } from './add_md2biom.nf'

// NOTE: We try to simplify the workflow by requiring the user to pre-train the classifier

workflow naive_bayes_workflow {
    take:
        // tuple val(meta), file('otu_table.biom'), file('rep_seqs.fasta'), file(samplemetadata_files)
        input_channel
    main:
        naive_bayes(
            input_channel,
            params.tax_assignment.assign['naive_bayes']['classifier']
        )
        add_md2biom(naive_bayes.out)
    emit:
        // add_md2biom has publishDir
        // tuple val(meta), file("otu_table_wtax.biom")
        add_md2biom.out
}
