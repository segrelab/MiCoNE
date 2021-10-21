// -*- mode:groovy -*-
// vim:ft=groovy

nextflow.enable.dsl=2

// Include workflows
include { sequence_processing_single_workflow } from './nf_micone/modules/sequence_processing/sequence_processing_single_workflow.nf'
include { sequence_processing_paired_workflow } from './nf_micone/modules/sequence_processing/sequence_processing_paired_workflow.nf'
include { denoise_cluster_workflow } from './nf_micone/modules/denoise_cluster/denoise_cluster_workflow.nf'
include { tax_assignment_workflow } from './nf_micone/modules/tax_assignment/tax_assignment_workflow.nf'
include { otu_processing_workflow } from './nf_micone/modules/otu_processing/otu_processing_workflow.nf'
include { network_inference_workflow } from './nf_micone/modules/network_inference/network_inference_workflow.nf'

// Include data ingestion functions
include { spp_data_ingestion } from './nf_micone/modules/utils/spp_data_ingestion.nf'
include { sps_data_ingestion } from './nf_micone/modules/utils/sps_data_ingestion.nf'

// Channels for samplesheets
Channel
    .fromPath(params.input)
    .set { input_channel }

workflow {
    ingestion = params.paired_end ? spp_data_ingestion : sps_data_ingestion
    sequence_processing_workflow = params.paired_end ? sequence_processing_paired_workflow : sequence_processing_single_workflow
    input_channel \
        | ingestion \
        | sequence_processing_workflow \
        | denoise_cluster_workflow \
        | tax_assignment_workflow \
        | otu_processing_workflow \
        | network_inference_workflow
}
