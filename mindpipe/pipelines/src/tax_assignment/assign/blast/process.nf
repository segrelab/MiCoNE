#!/usr/bin/env nextflow

// Initialize variables
def otu_table = params.otu_table
def sequence_16s_representative = params.sequence_16s_representative
def output_dir = file(params.output_dir)


// Parameters
def blast_ncpus = params.blast_ncpus
def parser_ncpus = params.parser_ncpus
def evalue_cutoff = params.evalue_cutoff
def n_hits = params.n_hits
def blast_db = file(params.blast_db)
def tax_map = file(params.tax_map)


// Channels
Channel
    .fromPath(otu_table)
    .map { tuple(it.getParent().baseName, it) }
    .set { chnl_otu_table }

Channel
    .fromPath(sequence_16s_representative)
    .map { tuple(it.getParent().baseName, it) }
    .set { chnl_rep_seqs }


// Processes

// Step1: Blast representative sequences against the blast database
process blast {
    tag "${id}"
    publishDir "${output_dir}/blast/${id}"
    input:
    set val(id), file(rep_seqs) from chnl_rep_seqs
    output:
    set val(id), file("blast_output.xml") into chnl_blast_results
    script:
    {{ blast }}
}

// Step2: Parse the blast results and obtain consensus taxonomy for each rep_seq
process parser {
    tag "${id}"
    input:
    set val(id), file(blast_output) from chnl_blast_results
    output:
    set val(id), file("tax_assignment.tsv")  into chnl_tax_assignment
    script:
    {{ parser }}
}

chnl_otu_table
    .join(chnl_tax_assignment)
    .set { chnl_combined_data }

// Step3: Attach the taxonomy assignment to the OTU table
process addtax2biom {
    tag "${id}"
    publishDir "${output_dir}/blast/${id}", saveAs: { "otu_table.biom" }
    input:
    set val(id), file(otu_table), file(tax_assignment) from chnl_combined_data
    output:
    set val(id), file("otu_table_wtax.biom") into chnl_output
    script:
    {{ addtax2biom }}
}
