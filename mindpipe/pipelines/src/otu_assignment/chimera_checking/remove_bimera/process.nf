#!/usr/bin/env nextflow

// Initialize variables
def otu_table = params.otu_table
def sequence_16s_representative = params.sequence_16s_representative
def output_dir = file(params.output_dir)


// Parameters
def chimera_method = params.chimera_method
def ncpus = params.ncpus


// Channels
Channel
    .fromPath(otu_table)
    .ifEmpty { exit 1, "OTU table not found in channel" }
    .map { tuple(it.getParent().baseName, it) }
    .set { chnl_otutable }

Channel
    .fromPath(sequence_16s_representative)
    .ifEmpty { exit 1, "Representative sequences not found in channel" }
    .map { tuple(it.getParent().baseName, it) }
    .set { chnl_repseqs  }

chnl_otutable
    .join(chnl_repseqs)
    .set { chnl_input }

// Processes

// Step1: Create a sequence table
process create_seqtable {
    tag "${id}"
    input:
    set val(id), file(otutable_file), file(repseqs_file) from chnl_input
    output:
    set val(id), file('seq_table.tsv') into chnl_seqtable
    script:
    {{ create_seqtable }}
}

// Step2: Remove chimeras using removeBimeraDenovo
process remove_chimeras {
    tag "${id}"
    input:
    set val(id), file(seqtable_file) from chnl_seqtable
    output:
    set val(id), file("unhashed_otu_table.biom"), file("unhashed_rep_seqs.fasta") into chnl_biomseq
    script:
    {{ remove_chimeras }}
}

// Step3: Rehash the sequence ids
process hashing {
    tag "${id}"
    publishDir "${output_dir}/${id}", mode: 'copy', overwrite: true
    input:
    set val(id), file(unhashed_otu_table), file(unhashed_rep_seqs) from chnl_biomseq
    output:
    set val(id), file("otu_table.biom"), file("rep_seqs.fasta") into chnl_output
    script:
    {{ hashing }}
}
