// Main variables to be defined
// NOTE: These should be defined before any include statements

// Tax assignment imports
include { naive_bayes_workflow } from './assign/naive_bayes_workflow.nf'
include { blast_workflow } from './assign/blast_workflow.nf'

// Main workflow
workflow tax_assignment_workflow {
    take:
        // tuple val(meta), file('otu_table.biom'), file('rep_seqs.fasta'), file(samplemetadata_files)
        input_channel
    main:
        input_channel \
            | (naive_bayes_workflow & blast_workflow)
        output_channel = blast_workflow.out
                            .mix(naive_bayes_workflow.out)
    emit:
        // tuple val(meta), file("otu_table_wtax.biom")
        output_channel
}
