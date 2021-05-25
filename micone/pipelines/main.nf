nextflow.enable.dsl=2

// Include workflows
include { denoise_cluster_workflow } from './modules/denoise_cluster/denoise_cluster_workflow.nf'
include { tax_assignment_workflow } from './modules/tax_assignment/tax_assignment_workflow.nf'
include { otu_processing_workflow } from './modules/otu_processing/otu_processing_workflow.nf'
include { network_inference_workflow } from './modules/network_inference/network_inference_workflow.nf'


// Include data ingestion functions

// TODO: Channels here

workflow {
    input_channel \
        | denoise_cluster_workflow \
        | tax_assignment_workflow \
        | otu_processing_workflow \
        | network_inference_workflow
}
