#!/usr/bin/env nextflow

// Initialize variables
def otu_table = params.otu_table
def sequence_16s_representative = params.sequence_16s_representative
def output_dir = file(params.output_dir)


// Parameters


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

// Step1: Import files as artifacts
process import_files {
    tag "${id}"
    input:
    set val(id), file(otu_table), file(rep_seqs) from chnl_input
    output:
    set val(id), file("otu_table.qza"), file("rep_seqs.qza") into chnl_biomseq
    script:
    {{ import_files }}
}

// Step2: Remove chimeras using vserach uchime-denovo
process remove_chimeras {
    tag "${id}"
    input:
    set val(id), file(otutable_artifact), file(repseqs_artifact) from chnl_biomseq
    output:
    set val(id), file("otu_table_nonchimeric.qza"), file("rep_seqs_nonchimeric.qza") into chnl_nonchimeric
    script:
    {{ remove_chimeras }}
}

// Step3: Export files
process export_files {
    tag "${id}"
    publishDir "${output_dir}/${id}", mode: 'copy', overwrite: true
    input:
    set val(id), file(otutable_nonchimeric), file(repseqs_nonchimeric) from chnl_nonchimeric
    output:
    set val(id), file("otu_table.biom"), file("rep_seqs.fasta") into chnl_output
    script:
    {{ export_files }}
}
