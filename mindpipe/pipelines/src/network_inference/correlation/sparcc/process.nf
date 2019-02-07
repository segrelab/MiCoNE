#!/usr/bin/env nextflow

// Initialize variables
def otudata = params.otudata
def output_dir = file(params.output_dir)

// Parameters
def iterations = params.iterations
def bootstraps = params.bootstraps

Channel
    .fromPath(otudata)
    .ifEmpty {exit 1, "Otu files not found"}
    .map { tuple(it.baseName, it) }
    .set { chnl_otudata_biom }

process biom2tsv {
    tag "$id"

    input:
    set val(id), file(otu_file) from chnl_otudata_biom

    output:
    set val(id), file('*.tsv') into chnl_otudata_corr, chnl_otudata_resamp, chnl_otudata_pval

    script:
    {{ biom2tsv }}
}


process compute_correlations {
    tag "${id}"
    publishDir "${output_dir}"

    input:
    set val(id), file(otu_file) from chnl_otudata_corr

    output:
    set val(id), file('*_corr.tsv') into corr_pval

    script:
    {{ compute_correlations }}
}

process resampling {
    tag "${id}"

    input:
    set val(id), file(otu_file) from chnl_otudata_resamp

    output:
    set val(id), file('*.tsv') into resamplings

    script:
    {{ resampling }}
}

// TODO: Maybe instead of this we can use GNU parallel to run in parallel in single job
resamplings
    .map { id, resamp ->
            resamp.collect { resampid -> [id, resampid] }
    }
    .flatMap {it}
    .set { resamplings_bootstrap_corrs }

process bootstrapping {
    tag "${id}|${resample.baseName}"

    input:
    set val(id), file(resample) from resamplings_bootstrap_corrs

    output:
    set val(id), file('*_corr.boot') into chnl_bootstraps

    script:
    {{ bootstrapping }}
}

chnl_bootstraps
    .groupTuple()
    .join(corr_pval, by: 0)
    .join(chnl_otudata_pval, by: 0)
    .set { pval_input_chnl }

process calculate_pvalues {
    tag "${id}"
    publishDir "${output_dir}"

    input:
    set val(id), file(boot_file), file(corr_file), file(otu_file) from pval_input_chnl

    output:
    set val(id), file('*_pval.tsv') into pval

    script:
    // def bstrap = bootstraps?.find{it}.baseName.split('_')?.find{it} + "_level_#.boot"
    {{ calculate_pvalues }}
}
