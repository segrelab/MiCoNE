#!/usr/bin/env nextflow

// Initialize variables
def otu_table = params.otu_table
def sequence_16s_representative = params.sequence_16s_representative
def sample_metadata = params.sample_metadata
def output_dir = file(params.output_dir)


// Parameters
def reference_sequences = params.reference_sequences
def tax_map = params.tax_map
def classifier = params.classifier
def ncpus = params.ncpus
def confidence = params.confidence


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

// Step1: Train classifier on reference_sequences and taxonomy_map
if(classifier) {
    Channel
        .fromPath(classifier)
        .set { chnl_classifier_artifact }
} else {
    process train_classifier {
        output:
        file('classifier.qza') into chnl_classifier_artifact
        script:
        {{ train_classifier }}
    }
}

chnl_rep_seqs
    .combine(chnl_classifier_artifact)
    .set { chnl_repseqs_classifier }

// Step2: Assign taxonomy using the classifier
process assign_taxonomy {
    tag "${id}"
    publishDir "${output_dir}/${id}", mode: 'copy', overwrite: true
    input:
    set val(id), file(rep_seqs), file(classifier) from chnl_repseqs_classifier
    output:
    set val(id), file('taxonomy.tsv') into chnl_taxonomy
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
