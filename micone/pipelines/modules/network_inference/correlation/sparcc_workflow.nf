include { resample } from './../bootstrap/resample.nf'
include { sparcc } from './sparcc.nf'
include { pvalues } from './../bootstrap/pvalue.nf'

workflow sparcc_workflow {
    take:
        // tuple val(id), file(otu_table)
        otu_table_channel
    main:
        otu_table_channel | sparcc
        // TODO: Maybe include an if statement for the resampling
        otu_table_channel | resample
        pvalues(sparcc.out, resample.out)
    emit:
        // has `publishDir` -> ${params.output_dir}/${task.process}/${id}
        pvalues.out
}
