#!/usr/bin/env nextflow

// Initialize variables
def sequence_artifacts = params.sequence_artifacts
def output_dir = file(params.output_dir)


// Parameters
n_threads = params.n_threads  // --p-n-threads
max_ee = params.max_ee  // --p-max-ee
trunc_q = params.trunc_q  // --p-trunc-q


// Channels
Channel
    .fromPath(sequence_artifacts)
    .ifEmpty { exit 1, "Sequence artifacts not found" }
    .into { sequence_artifact_viz; sequence_artifact_type; sequence_artifact_dada2 }


// Processes
process get_visualization {
    tag "visualization"
    publishDir "${output_dir}/visualization"

    input:
    file sequence_artifact from sequence_artifact_viz

    output:
    file ('output/*-seven-number-summaries.csv') into sequence_viz_chnl

    script:
    {{ get_visualization }}
}

process get_filetype {
    tag "filetype"
    publishDir "${output_dir}/filetype"

    input:
    file sequence_artifact from sequence_artifact_type

    output:
    file ('filetype.txt') into (filetype_quality, filetype_dada2)

    script:
    {{ get_filetype }}
}

process quality_analysis {
    tag "quality_analysis"
    publishDir "${output_dir}/quality_analysis"

    input:
    val filetype from filetype_quality
    file summaries from sequence_viz_chnl

    output:
    file ('trim.txt') into quality_cmd_chnl

    script:
    def itype = filetype.text.contains('SingleEnd') ? 'single' : 'paired'
    // NOTE: Here we assumed that the summaries just get copied over
    def forward = "forward-seven-number-summaries.csv"
    def reverse = itype == 'paired' ? "reverse-seven-number-summaries.csv" : ""
    {{ quality_analysis }}
}

process dada2 {
    tag "dada2"
    publishDir "${output_dir}/dada2"

    input:
    file sequence_artifact from sequence_artifact_dada2
    val filetype from filetype_dada2
    val quality_cmd from quality_cmd_chnl

    output:
    file('*.qza') into output_chnl

    script:
    def itype = filetype.text.contains('SingleEnd') ? 'single' : 'paired'
    def trim_cmd = quality_cmd.text
    {{ dada2 }}
}
