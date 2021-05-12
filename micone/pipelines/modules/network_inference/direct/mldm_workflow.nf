include { mldm } from './mldm.nf'

workflow mldm_workflow {
    take:
        // tuple val(id), file(otu_table)
        otu_table_channel
    main:
        otu_table_channel | mldm
    emit:
        // has `publishDir` -> ${params.output_dir}/${task.process}/${id}
        mldm.out
}
