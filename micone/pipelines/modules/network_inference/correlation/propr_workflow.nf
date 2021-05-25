include { resample } from './../bootstrap/resample.nf'
include { propr } from './propr.nf'
include { pvalues } from './../bootstrap/pvalue.nf'

workflow propr_workflow {
    take:
        // tuple val(meta), file(otu_file), file(obs_metadata), file(sample_metadata), file(children_map)
        input_channel
    main:
        input_channel \
            | resample \
            | propr \
            | pvalues
    emit:
        // propr and pvalues have publishDir
        // tuple val(meta), file(corr_file), file(pvalue_file), file(obs_metadata), file(sample_metadata), file(children_map)
        pvalues.out
}
