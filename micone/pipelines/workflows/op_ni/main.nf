// -*- mode:groovy -*-
// vim:ft=groovy

nextflow.enable.dsl=2

// Include workflows
include { otu_processing_workflow } from './nf_micone/modules/otu_processing/otu_processing_workflow.nf'
include { network_inference_workflow } from './nf_micone/modules/network_inference/network_inference_workflow.nf'

// Include data ingestion functions
include { op_data_ingestion } from './nf_micone/modules/utils/op_data_ingestion.nf'

// Channels for samplesheets
Channel
    .fromPath(params.input)
    .set { input_channel }

workflow {
    input_channel \
        | op_data_ingestion \
        | otu_processing_workflow \
        | network_inference_workflow
}
