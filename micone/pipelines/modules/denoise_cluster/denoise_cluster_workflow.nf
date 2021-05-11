// Sequencing processing imports
// QUESTION: What about `join_reads`(?)
include { demultiplexing_454_workflow } from './sequence_processing/demultiplexing_454_workflow.nf'
include { demultiplexing_illumina_workflow } from './sequence_processing/demultiplexing_illumina_workflow.nf'
include { trim_filter_fixed_workflow } from './sequence_processing/trim_filter_fixed_workflow.nf'

// Denoising clustering imports
include { closed_reference_workflow } from './denoise_cluster/closed_reference_workflow.nf'
include { dada2_workflow } from './denoise_cluster/dada2_workflow.nf'
include { deblur_workflow } from './denoise_cluster/deblur_workflow.nf'
include { de_novo_workflow } from './denoise_cluster/de_novo_workflow.nf'
include { open_reference_workflow } from './denoise_cluster/open_reference_workflow.nf'

// Chimera checking imports
include { uchime_workflow } from './chimera_checking/uchime_workflow.nf'
include { remove_bimera_workflow } from './chimera_checking/remove_bimera_workflow.nf'


// Main variables to be defined in params
// dc_tools
// chimera_tools


// Main workflow
workflow denoise_cluster_workflow {
    take:
        // tuple val(id), file(sequence_files), file(barcode_files), file(barcode_sample_mapping)
        input_channel
    main:
        if dc_tools == ["dada2", "deblur", "open_reference", "de_novo", "closed_reference"] {
            input_channel \
            demultiplexing_illumina_workflow \
            trim_filter_fixed_workflow \
            (dada2_workflow & deblur_workflow & open_reference_workflow & de_novo_workflow & closed_reference_workflow) \
            mix \
            (uchime_workflow & remove_bimera_workflow)
        }
        input_channel \
            | create_seqtable \
            | remove_bimera \
            | hashing3
    emit:
        // has `publishDir` -> ${params.output_dir}/${task.process}/${id}
        hashing3.out
}
