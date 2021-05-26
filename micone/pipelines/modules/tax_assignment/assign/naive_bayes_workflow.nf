include { naive_bayes } from './naive_bayes.nf'
include { add_md2biom } from './add_md2biom.nf'

// NOTE: We try to simplify the workflow by requiring the user to pre-train the classifier

workflow naive_bayes_workflow {
    take:
        // tuple val(meta), file('otu_table.biom'), file('rep_seqs.fasta'), file(samplemetadata_files)
        input_channel
    main:
        input_channel \
            | naive_bayes \
            | add_md2biom
    emit:
        // add_md2biom has publishDir
        // tuple val(meta), file("otu_table_wtax.biom")
        add_md2biom.out
}
