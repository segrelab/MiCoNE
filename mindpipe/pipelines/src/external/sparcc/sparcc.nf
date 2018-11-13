#!/usr/bin/env nextflow

// Initialize variables
def otudata = params.otudata
def sample_metadata = params.sample_metadata
def lineagedata = params.lineagedata
def childrendata = params.childrendata
def output_dir = file(params.output_dir)

/*
NOTE: Even though we need only otudata for this process we take metadata and taxondata
as input because these are needed by the subsequent processes
*/

// Parameters
def niters = params.niters
def nboots = params.nboots

Channel
    .fromPath(otudata)
    .ifEmpty {exit 1, "Otu files not found"}
    .map {
        tuple(
            it.getParent().toString().split("/")[-1],
            it.baseName.split("_otudata")[0],
            it
        )
    }
    .into { otudata_chnl_corr; otudata_chnl_resamp }

Channel
    .fromPath(sample_metadata)
    .ifEmpty {exit 1, "Metadata files not found"}
    .map {
        tuple(
            it.getParent().toString().split("/")[-1],
            it.baseName.split("_sample_metadata")[0],
            it
        )
    }
    .into { metadata_chnl_all; metadata_chnl_otu }

Channel
    .fromPath(lineagedata)
    .ifEmpty {exit 1, "Taxondata files not found"}
    .map {
        tuple(
            it.getParent().toString().split("/")[-1],
            it.baseName.split("_taxondata")[0],
            it
        )
    }
    .into { taxondata_chnl_all; taxondata_chnl_otu }

Channel
    .fromPath(childrendata)
    .ifEmpty {exit 1, "Childrendata files not found"}
    .map {
        tuple(
            it.getParent().toString().split("/")[-1],
            it.baseName.split("_children")[0],
            it
        )
    }
    .set { childrendata_chnl }

process compute_correlations {
    tag "${id}|${level}"
    publishDir "${output_dir}/compute_correlations/${id}"

    input:
    set val(id), val(level), file(otu_file) from otudata_chnl_corr

    output:
    set val(id), val(level), file('*_corr.tsv') into corr_pval
    set val(id), val(level), file('*.log') into correlation_log

    script:
    {{ compute_correlations }}
}

process resampling {
    tag "${id}|${level}"
    publishDir "${output_dir}/resampling/${id}/${level}"

    input:
    set val(id), val(level), file(otu_file) from otudata_chnl_resamp

    output:
    set val(id), val(level), file('*.resamp') into resamplings

    script:
    {{ resampling }}
}

resamplings
    .map { id, level, resamp ->
            resamp.collect { resampid -> [id, level, resampid] }
    }
    .flatMap {it}
    .set { resamplings_bootstrap_corrs }

process bootstrapping {
    tag "${id}|${resample.baseName}"
    publishDir "${output_dir}/bootstrapping/${id}/${level}"

    input:
    set val(id), val(level), file(resample) from resamplings_bootstrap_corrs

    output:
    set val(id), val(level), file('*.boot') into bootstraps
    set val(id), val(level), file('*.log') into boot_logs

    script:
    {{ bootstrapping }}
}

bootstraps
    .groupTuple(by: [0, 1])
    .join(corr_pval, by: [0, 1])
    .set { pval_input_chnl }

process calculate_pvalues {
    tag "${id}|${level}"
    publishDir "${output_dir}/calculate_pvalues/${id}"

    input:
    set val(id), val(level), file(bootstraps), file(correlation) from pval_input_chnl

    output:
    set val(id), val(level), file('*_pval.tsv') into pval

    script:
    def bstrap = bootstraps?.find{it}.baseName.split('_')?.find{it} + "_level_#.boot"
    {{ calculate_pvalues }}
}

// TODO: Refactor these later: Use remainder: true?
metadata_chnl_all
    .join(taxondata_chnl_all, by: [0, 1])
    .join(childrendata_chnl, by: [0, 1])
    .set { passthrough_chnl_all }

process passthrough_all {
    tag "${id}|${level}"

    input:
    set val(id), val(level), file(metadata_file), file(taxondata_file), file(children_file) from passthrough_chnl_all

    script:
    """
    mkdir -p ${output_dir}/passthrough/${id}
    cp $metadata_file ${output_dir}/passthrough/${id}/${metadata_file}
    cp $taxondata_file ${output_dir}/passthrough/${id}/${taxondata_file}
    cp $children_file ${output_dir}/passthrough/${id}/${children_file}
    """
}

metadata_chnl_otu
    .join(taxondata_chnl_otu, by: [0, 1])
    .filter { it[1] == 'OTU_level' }
    .set { passthrough_chnl_otu }

process passthrough_otu {
    tag "${id}|${level}"

    input:
    set val(id), val(level), file(metadata_file), file(taxondata_file) from passthrough_chnl_otu

    script:
    """
    mkdir -p ${output_dir}/passthrough/${id}
    cp $metadata_file ${output_dir}/passthrough/${id}/${metadata_file}
    cp $taxondata_file ${output_dir}/passthrough/${id}/${taxondata_file}
    """
}