include { resample } from './../bootstrap/resample.nf'
include { spearman } from './spearman.nf'
include { pvalues } from './../bootstrap/pvalue.nf'

workflow spearman_workflow {
    take:
        // tuple val(meta), file(otu_file), file(obs_metadata), file(sample_metadata), file(children_map)
        input_channel
    main:
        input_channel \
            | resample \
            | spearman \
            | pvalues
    emit:
        // spearman and pvalues have publishDir
        // tuple val(meta), file(corr_file), file(pvalue_file), file(obs_metadata), file(sample_metadata), file(children_map)
        pvalues.out
}
