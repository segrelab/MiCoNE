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
include { cozine_workflow } from './direct/cozine_workflow.nf'
include { harmonies_workflow } from './direct/harmonies_workflow.nf'
include { spring_workflow } from './direct/spring_workflow.nf'

// Network imports
include { make_network_with_pvalue } from './network/make_network_with_pvalue.nf'
include { make_network_without_pvalue } from './network/make_network_without_pvalue.nf'
include { merge_pvalues } from './network/merge_pvalues.nf'
include { create_consensus } from './network/create_consensus.nf'

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
            & mldm_workflow \
            & cozine_workflow \
            & harmonies_workflow \
            & spring_workflow )

    // NOTE: These will have have extra pvalue
    corr_output = sparcc_workflow.out
                    .mix(
                        pearson_workflow.out,
                        spearman_workflow.out,
                        propr_workflow.out,
                    )
    // NOTE: These will not have pvalue
    direct_output = spieceasi_workflow.out
                        .mix(
                            flashweave_workflow.out,
                            mldm_workflow.out,
                            cozine_workflow.out,
                            harmonies_workflow.out,
                            spring_workflow.out
                        )

    // Correlation method output
    make_network_with_pvalue(corr_output)
    merge_pvalues(make_network_with_pvalue.out.collect())

    // Direct method output
    make_network_without_pvalue(direct_output)

    // Create consensus
    network_channel = merge_pvalues.out.flatten().mix(make_network_without_pvalue.out)
    create_consensus(network_channel.collect())


    emit:
        // all processes have publishDir
        // tuple val(meta), file("*.json")
        create_consensus.out
}
