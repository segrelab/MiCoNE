#!/usr/bin/env nextflow

// Initialize variables
def sequence_16s = params.sequence_16s
def sample_sequence_manifest = params.sample_sequence_manifest
def output_dir = file(params.output_dir)


// Parameters
def ncpus = params.ncpus
def min_reads = params.min_reads
def min_size = params.min_size


// Channels
Channel
    .fromPath(sequence_16s)
    .ifEmpty { exit 1, "Sequences not found in channel" }
    .map { tuple(it.getParent().baseName, it) }
    .groupTuple()
    .set { chnl_sequences }

Channel
    .fromPath(sample_sequence_manifest)
    .ifEmpty { exit 1, "Manifest files not found in channel"  }
    .map { tuple(it.getParent().baseName, it) }
    .groupTuple()
    .set { chnl_manifest }

chnl_sequences
    .join(chnl_manifest)
    .set { chnl_seqcollection }


// Processes

// Step1: Denoise using deblur
process import_sequences {
    tag "${id}"
    publishDir "${output_dir}/${id}", mode: 'copy', overwrite: true
    input:
    set val(id), file(sequence_files), file(manifest_file) from chnl_seqcollection
    output:
    set val(id), file('*_otu_table.biom'), file('*_rep_seqs.fasta') into chnl_biomseq_hashing
    script:
    {{ deblur }}
}

// Step2: Replace the ids with hashes of the sequences
process deblur {
    tag "${id}"
    publishDir "${output_dir}/${id}", mode: 'copy', overwrite: true
    input:
    set val(id), file(unhashed_otu_table), file(unhashed_rep_seqs) from chnl_biomseq_hashing
    output:
    set val(id), file('otu_table.biom'), file('rep_seqs.fasta') into chln_output
    script:
    {{ hashing }}
}
