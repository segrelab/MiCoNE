include { resample } from './../bootstrap/resample.nf'
include { pearson } from './pearson.nf'
include { pvalues } from './../bootstrap/pvalue.nf'

workflow pearson_workflow {
    take:
        // tuple val(id), file(otu_table)
        otu_table_channel
    main:
        otu_table_channel | pearson
        // TODO: Maybe include an if statement for the resampling
        otu_table_channel | resample
        pvalues(pearson.out, resample.out)
    emit:
        // has `publishDir` -> ${params.output_dir}/${task.process}/${id}
        pvalues.out
}
