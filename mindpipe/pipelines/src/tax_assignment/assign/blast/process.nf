#!/usr/bin/env nextflow

// Initialize variables
def otu_table = params.otu_table
def sequence_16s_representative = params.sequence_16s_representative
def sample_metadata = params.sample_metadata
def output_dir = file(params.output_dir)


// Parameters
def reference_sequences = file(params.reference_sequences)
def tax_map = file(params.tax_map)
def max_accepts = params.max_accepts
def perc_identity = params.perc_identity
def evalue = params.evalue
def min_consensus = params.min_consensus


// Channels
Channel
    .fromPath(otu_table)
    .map { tuple(it.getParent().baseName, it) }
    .set { chnl_otu_table }

Channel
    .fromPath(sequence_16s_representative)
    .map { tuple(it.getParent().baseName, it) }
    .set { chnl_rep_seqs }

Channel
    .fromPath(sample_metadata)
    .map { tuple(it.getParent().baseName, it) }
    .set { chnl_sample_metadata }


// Processes

// Step1a: Import files
process import_reads {
    tag "${id}"
    input:
    set val(id), file(rep_seqs) from chnl_rep_seqs
    output:
    set val(id), file('rep_seqs.qza') into chnl_repseqs_artifact
    script:
    {{ import_reads }}
}

// Step1b: Import references
process import_references {
    output:
    set file('tax_map.qza'), file('reference_sequences.qza') into chnl_reftax_artifact
    script:
    {{ import_references }}
}

chnl_repseqs_artifact
    .combine(chnl_reftax_artifact)
    .set { chnl_repseqs_reftax }

// Step2: Blast representative sequences against the blast database
process assign_taxonomy {
    tag "${id}"
    publishDir "${output_dir}/${id}", mode: 'copy', overwrite: true
    input:
    set val(id), file(repseq_artifact), file(taxmap_artifact), file(refseq_artifact) from chnl_repseqs_reftax
    output:
    set val(id), file("taxonomy.tsv") into chnl_taxonomy
    script:
    {{ assign_taxonomy }}
}

chnl_otu_table
    .join(chnl_taxonomy)
    .join(chnl_sample_metadata)
    .set { chnl_otu_md }

// Step3: Attach the observation and sample metadata to the OTU table
process add_md2biom {
    tag "${id}"
    publishDir "${output_dir}/${id}", saveAs: { "otu_table.biom" }, mode: 'copy', overwrite: true
    input:
    set val(id), file(otu_table_file), file(tax_assignment), file(sample_metadata_file) from chnl_otu_md
    output:
    set val(id), file("otu_table_wtax.biom") into chnl_output
    script:
    {{ add_md2biom }}
}
