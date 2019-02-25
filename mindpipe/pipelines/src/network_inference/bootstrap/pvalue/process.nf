#!/usr/bin/env nextflow

// Initialize variables
def otudata = params.otudata
def correlation_table = params.interaction_table
def output_dir = file(params.output_dir)

// Parameters
def threads = params.threads


// Channels

Channel
    .fromPath(otudata)
    .ifEmpty { exit 1, "Otu files not found" }
    .map { tuple(
        (it.getParent().getParent().baseName + '_' + it.getParent().baseName),
        it.getParent().getParent().baseName,
        it.getParent().baseName,
        it
    ) }
    .groupTuple()
    .set { chnl_otudata }

Channel
    .fromPath(correlation_table)
    .ifEmpty { exit 1, "Correlation files not found" }
    .map { tuple(
        (it.getParent().getParent().baseName + '_' + it.getParent().baseName),
        it
    ) }
    .groupTuple()
    .set { chnl_correlation_table }

chnl_otudata
    .join(chnl_correlation_table, by: 0)
    .set { chnl_input }


// Processes

process calculate_pvalues {
    tag "${id}"
    publishDir "${output_dir}/${dataset[0]}"
    input:
    set val(id), val(dataset), val(level), file(otu_file), file(corr_file) from chnl_input
    output:
    set val(id), file('*_pval.tsv') into chnl_pval
    script:
    def level_str = level[0]
    {{ calculate_pvalues }}
}
