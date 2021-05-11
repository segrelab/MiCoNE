include { naive_bayes } from './naive_bayes.nf'
include { add_md2biom } from './add_md2biom.nf'

// NOTE: We try to simplify the workflow by requiring the user to pre-train the classifier

workflow blast_workflow {
    take:
        // tuple val(id), file(rep_seqs)
        rep_seqs_channel
        // tuple val(id), file(sample_metadata)
        otu_table_channel
        // tuple val(id), file(sample_metadata)
        sample_metadata_channel
        // TODO: rep_seqs, otu_table and sample_metadata should ideally be in one channel
        // otu_table and rep_seqs come out of the same channel but sample_metadata is input
    main:
        // TODO: The classifier object should be passed in as `${params.naive_bayes.classifier}`
        rep_seqs_channel \
            | naive_bayes \
            | join(otu_table_channel) \
            | join(sample_metadata_channel) \
            | add_md2biom
    emit:
        // has `publishDir` -> ${params.output_dir}/${task.process}/${id}
        add_md2biom.out
}
