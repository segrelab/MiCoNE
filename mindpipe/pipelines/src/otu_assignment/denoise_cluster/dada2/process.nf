#!/usr/bin/env nextflow

// Initialize variables
def sequence_16s = params.sequence_16s
def sample_sequence_manifest = params.sample_sequence_manifest
def output_dir = file(params.output_dir)


// Parameters
def ncpus = params.ncpus
def big_data = params.big_data


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
process dada2 {
    tag "${id}"
    publishDir "${output_dir}/dada2/${id}"
    input:
    set val(id), file(sequence_files), file(manifest_file) from chnl_seqcollection
    output:
    set val(id), file('*.biom'), file('*.fasta') into chln_biomseq_hashing
    script:
    {{ dada2 }}
}

process hashing {
    tag "${id}"
    publishDir "${output_dir}/dada2/${id}"
    input:
    set val(id), file(unhashed_otu_table), file(unhashed_rep_seqs) from chln_biomseq_hashing
    output:
    set val(id), file('otu_table.biom'), file('rep_seqs.fasta') into chnl_output
    script:
    {{ hashing }}
}
