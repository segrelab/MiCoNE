#!/usr/bin/env nextflow

// Initialize variables
def artifacts = params.artifacts // QUESTION: How do we input any type of artifacts
def output_dir = file(params.output_dir)

// Parameters
def name = params.name

// Channels
Channel
    .fromPath(artifacts)
    .ifEmpty { exit 1, "Representative sequence artifacts not found" }
    .set { artifact_chnl }


// Processes
process export {
    tag "export"
    publishDir "${output_dir}"

    input:
    file artifact from  artifact_chnl

    output:
    file ('${dir_name}/*') into output_chnl

    script:
    def dir_name = (name != "") ? name : artifact.baseName
    {{ export }}
}