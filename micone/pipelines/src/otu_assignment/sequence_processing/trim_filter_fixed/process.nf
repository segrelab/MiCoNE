#!/usr/bin/env nextflow

// Initialize variables

def sequence_16s = params.sequence_16s
def sample_sequence_manifest = params.sample_sequence_manifest
def output_dir = params.output_dir


// Parameters

def seq_samplesize = params.seq_samplesize
def ncpus = params.ncpus
def max_ee = params.max_ee
def trunc_q = params.trunc_q


// Channels

Channel
    .fromPath(sequence_16s)
    .ifEmpty { exit 1, "Sequences not found in channel" }
    .map { tuple(it.getParent().baseName, it) }
    .groupTuple()
    .into { chnl_seqs; chnl_seqs_trim }

Channel
    .fromPath(sample_sequence_manifest)
    .ifEmpty { exit 1, "Manifest files not found in channel"  }
    .map { tuple(it.getParent().baseName, it) }
    .groupTuple()
    .into { chnl_manifest; chnl_manifest_trim }

chnl_seqs
    .join(chnl_manifest, by: 0)
    .set { chnl_seqcollection }


// Processes

// 1. Import the sequences to qiime2 artifacts
process import_sequences {
    tag "${id}"
    input:
    set val(id), file(sequence_files), file(manifest_file) from chnl_seqcollection
    output:
    set val(id), file('sequence_folder/*.qza') into chnl_seqartifact_viz
    script:
    {{ import_sequences }}
}

// 2. Obtain sampled quality profiles via demux viz
process export_visualization {
    tag "${id}"
    publishDir "${output_dir}/${id}/quality_summary", saveAs: { filename -> filename.split("/")[1] }, mode: 'copy', overwrite: true
    input:
    set val(id), file(sequence_artifact) from chnl_seqartifact_viz
    output:
    set val(id), file('output/forward-seven-number-summaries.csv') into chnl_qualsummary_analysis
    script:
    {{ export_visualization }}
}

// 3. Identify positions on the front and the tail that need to be trimmed based on
// a. quality and b. sequence retainment
process quality_analysis {
    tag "${id}"
    publishDir "${output_dir}/${id}/quality_summary", mode: 'copy', overwrite: true
    input:
    set val(id), file(qual_summary) from chnl_qualsummary_analysis
    output:
    set val(id), file('trim.txt') into chnl_trimcmd_trim
    script:
    {{ quality_analysis }}
}

// Join sequence_files, manifest_file and trim_cmd into one channel
chnl_seqs_trim
    .join(chnl_manifest_trim, by: 0)
    .join(chnl_trimcmd_trim, by: 0)
    .set { chnl_trim }

// 4. Trimming the sequences using cutadapt
process trimming {
    tag "${id}"
    publishDir "${output_dir}/${id}", saveAs: { filename -> filename.split("/")[1] }, mode: 'copy', overwrite: true
    input:
    set val(id), file(sequence_files), file(manifest_file), file(trim_cmd) from chnl_trim
    output:
    set val(id), file('trimmed/*.fastq.gz'), file('trimmed/MANIFEST') into chnl_output
    script:
    {{ trimming }}
}
