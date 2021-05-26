// Main variables to be defined
// NOTE: These should be defined before any include statements


// Sequencing processing imports
include { demultiplexing_illumina_workflow } from './sequence_processing/demultiplexing_illumina_workflow.nf'
include { trim_filter_fixed_workflow } from './sequence_processing/trim_filter_fixed_workflow.nf'

// Denoising clustering imports
include { closed_reference_workflow } from './otu_assignment/closed_reference_workflow.nf'
include { dada2_workflow } from './otu_assignment/dada2_workflow.nf'
include { deblur_workflow } from './otu_assignment/deblur_workflow.nf'
include { de_novo_workflow } from './otu_assignment/de_novo_workflow.nf'
include { open_reference_workflow } from './otu_assignment/open_reference_workflow.nf'

// Chimera checking imports
include { uchime_workflow } from './chimera_checking/uchime_workflow.nf'
include { remove_bimera_workflow } from './chimera_checking/remove_bimera_workflow.nf'


// Main workflow
workflow denoise_cluster_workflow {
    take:
        // tuple val(meta), file(sequence_files), file(barcode_files), file(mapping_files)
        input_channel
        // tuple val(meta), file(samplemetadata_files)
        samplemetadata_channel
    main:
        input_channel \
            | demultiplexing_illumina_workflow \
            | trim_filter_fixed_workflow \
            | (dada2_workflow & deblur_workflow & open_reference_workflow & de_novo_workflow & closed_reference_workflow) \
            | mix \
            | (uchime_workflow & remove_bimera_workflow)
        output_channel = uchime_workflow.out
                            .mix(remove_bimera_workflow.out)
                            .join(samplemetadata_channel)
    emit:
        // tuple val(meta), file('otu_table.biom'), file('rep_seqs.fasta'), file(samplemetadata_files)
        output_channel
}
