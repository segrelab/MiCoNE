#!/usr/bin/env nextflow

// Initialize variables
def repseq_artifacts = params.repseq_artifacts
def output_dir = file(params.output_dir)


// Parameters
classifier_artifact = file(params.classifier_artifact)
n_jobs = params.n_jobs
reads_per_batch = params.reads_per_batch


// Channels
Channel
    .fromPath(repseq_artifacts)
    .ifEmpty { exit 1, "Representative sequence artifacts not found" }
    .set { repseq_artifact_chnl }


// Processes
process taxonomy_assignment {
    tag "taxonomy_assignment"
    publishDir  "${output_dir}", mode: 'copy', overwrite: true

    input:
    file repseq_artifact from repseq_artifact_chnl

    output:
    file ('*taxonomy.qza') into output_chnl

    script:
    {{ taxonomy_assignment }}
}
