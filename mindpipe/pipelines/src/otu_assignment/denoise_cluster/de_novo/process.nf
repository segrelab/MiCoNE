#!/usr/bin/env nextflow

// Initialize variables
def sequence_16s = params.sequence_16s
def sample_sequence_manifest = params.sample_sequence_manifest
def output_dir = file(params.output_dir)


// Parameters
def parameters = file(params.parameters)
def ncpus = params.ncpus // "-a -O $ncpus"


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

// Step1: Convert fastq to fasta and merge
process fastq2fasta {
    tag "${id}"
    input:
    set val(id), file(sequence_files), file(manifest_file) from chnl_seqcollection
    output:
    set val(id), file("${id}.fasta") into chnl_fasta_de_novo
    script:
    {{ fastq2fasta }}
}

// Step2: de_novo OTU picking
process pick_de_novo_otus {
    tag "${id}"
    publishDir "${output_dir}/${id}", mode: 'copy', overwrite: true
    input:
    set val(id), file(fasta_file) from chnl_fasta_de_novo
    output:
    set val(id), file('unhashed_otu_table.biom'), file('unhashed_rep_seqs.fasta'), file('log*.txt') into chnl_closedref_output
    script:
    def parallel_option = ncpus > 1 ? "-a -O ${ncpus}" : ''
    {{ pick_de_novo_otus }}
}

// Step3: Replace the ids with the hashes of the sequences
process hashing {
    tag "${id}"
    publishDir "${output_dir}/${id}", mode: 'copy', overwrite: true
    input:
    set val(id), file(unhashed_otu_table), file(unhashed_rep_seqs), file(log) from chnl_closedref_output
    output:
    set val(id), file('otu_table.biom'), file('rep_seqs.fasta') into chnl_output
    script:
    {{ hashing }}
}
