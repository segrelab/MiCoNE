// Main variables to be defined
// NOTE: These should be defined before any include statements

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
        // tuple val(meta), file('trimmed/*.fastq.gz'), file('trimmed/MANIFEST'), file(sequence_metadata), file(samplemetadata_files)
        input_channel
    main:
        input_channel \
            | (dada2_workflow & deblur_workflow & open_reference_workflow & de_novo_workflow & closed_reference_workflow) \
            | mix \
            | (uchime_workflow & remove_bimera_workflow)
        output_channel = uchime_workflow.out.mix(remove_bimera_workflow.out)
    emit:
        // tuple val(meta), file('otu_table.biom'), file('rep_seqs.fasta'), file(samplemetadata_files)
        output_channel
}
