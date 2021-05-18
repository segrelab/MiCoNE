// Main variables to be defined
// NOTE: These should be defined before any include statements

// Correlation imports
include { sparcc_workflow } from './correlation/sparcc_workflow.nf'
include { pearson_workflow } from './correlation/pearson_workflow.nf'
include { spearman_workflow } from './correlation/spearman_workflow.nf'
include { propr_workflow } from './correlation/propr_workflow.nf'

// Direct imports
include { spieceasi_workflow } from './direct/spieceasi_workflow.nf'
include { flashweave_workflow } from './direct/flashweave_workflow.nf'
include { mldm_workflow } from './direct/mldm_workflow.nf'

// Network imports
include { make_network } from './network/make_network.nf'

// Main workflow
workflow network_inference_workflow {
    take:
        // tuple val(meta), file(otu_file), file(obs_metadata), file(sample_metadata), file(children_map)
        input_channel

    main:
    input_channel \
        | ( sparcc_workflow \
            & pearson_workflow \
            & spearman_workflow \
            & propr_workflow \
            & spieceasi_workflow \
            & flashweave_workflow \
            & mldm_workflow )

    // NOTE: These will have have extra pvalues
    corr_output = sparcc_workflow.out
                    .mix(
                        pearson_workflow.out,
                        spearman_workflow.out,
                        propr_workflow.out,
                    )
    // NOTE: These will not have pvalues
    direct_output = spieceasi_workflow.out
                        .mix(
                            flashweave_workflow.out,
                            mldm_workflow.out
                        )

    make_network_with_pvalues(corr_output)
    make_network_without_pvalues(direct_output)

    network_channel = make_network_with_pvalues.out.mix(make_network_without_pvalues)

    emit:
        // all processes have publishDir
        // tuple val(meta), file("*.json")
        network_channel
}
