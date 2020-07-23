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

// Step1: Denoise using dada2
process dada2 {
    tag "${id}"
    publishDir "${output_dir}/${id}", mode: 'copy', overwrite: true
    input:
    set val(id), file(sequence_files), file(manifest_file) from chnl_seqcollection
    output:
    set val(id), file("seq_table.tsv") into chnl_seqtable
    script:
    {{ dada2 }}
}

// Step2: Make representative sequences and biom table from sequence table
process make_biom_repseqs {
    tag "${id}"
    publishDir "${output_dir}/${id}", mode: 'copy', overwrite: true
    input:
    set val(id), file(seq_table_file) from chnl_seqtable
    output:
    set val(id), file('*.biom'), file('*.fasta') into chln_biomseq_hashing
    script:
    {{ make_biom_repseqs }}
}

// Step3: Replace the ids with hashes of the sequences
process hashing {
    tag "${id}"
    publishDir "${output_dir}/${id}", mode: 'copy', overwrite: true
    input:
    set val(id), file(unhashed_otu_table), file(unhashed_rep_seqs) from chln_biomseq_hashing
    output:
    set val(id), file('otu_table.biom'), file('rep_seqs.fasta') into chnl_output
    script:
    {{ hashing }}
}
