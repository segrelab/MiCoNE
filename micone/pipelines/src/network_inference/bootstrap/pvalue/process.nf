#!/usr/bin/env nextflow

// Initialize variables
def otudata = params.otudata
def correlation_table = params.interaction_table
def correlation_bootstrap = params.interaction_bootstrap
def output_dir = file(params.output_dir)

// Parameters
def ncpus = params.ncpus


// Channels

Channel
    .fromPath(otudata)
    .ifEmpty { exit 1, "Otu files not found" }
    .map { tuple(
        (it.getParent().baseName + '_' + it.baseName.split("_otu")[0]),
        it.getParent().baseName,
        it.baseName.split("_otu")[0],
        it
    ) }
    .set { chnl_otudata }

Channel
    .fromPath(correlation_table)
    .ifEmpty { exit 1, "Correlation files not found" }
    .map { tuple(
        (it.getParent().baseName + '_' + it.baseName.split("_corr")[0]),
        it
    ) }
    .set { chnl_correlation_table }

Channel
    .fromPath(correlation_bootstrap)
    .ifEmpty { exit 1, "Correlation bootstraps not found" }
    .map { tuple(
        (it.getParent().getParent().baseName + '_' + it.getParent().baseName),
        it
    ) }
    .groupTuple()
    .set { chnl_correlation_bootstrap }

chnl_otudata
    .join(chnl_correlation_table, by: 0)
    .join(chnl_correlation_bootstrap, by: 0)
    .set { chnl_input }


// Processes

process calculate_pvalues {
    tag "${id}"
    publishDir "${output_dir}/${dataset}", mode: 'copy', overwrite: true
    input:
    set val(id), val(dataset), val(level), file(otu_file), file(corr_file), file(corr_bootstrap) from chnl_input
    output:
    set val(id), file('*_pval.tsv') into chnl_pval
    script:
    {{ calculate_pvalues }}
}
