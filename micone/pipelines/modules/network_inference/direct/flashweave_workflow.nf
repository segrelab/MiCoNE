include { flashweave } from './flashweave.nf'
include { flashweave } from './export_gml.nf'

workflow flashweave_workflow {
    take:
        // tuple val(id), file(otu_table)
        otu_table_channel
    main:
        otu_table_channel | flashweave | export_gml
    emit:
        // has `publishDir` -> ${params.output_dir}/${task.process}/${id}
        export_gml.out
}
