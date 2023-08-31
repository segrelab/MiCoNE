// -*- mode:groovy -*-
// vim:ft=groovy

nextflow.enable.dsl=2

// Include workflows
include { network_inference_workflow } from './nf_micone/modules/network_inference/network_inference_workflow.nf'

// Include data ingestion functions
include { ni_data_ingestion } from './nf_micone/modules/utils/ni_data_ingestion.nf'

// Channels for samplesheets
Channel
    .fromPath(params.input)
    .set { input_channel }

workflow {
    input_channel \
        | ni_data_ingestion \
        | network_inference_workflow
}
