include { spieceasi } from './spieceasi.nf'

workflow spieceasi_workflow {
    take:
        // tuple val(id), file(otu_table)
        otu_table_channel
    main:
        otu_table_channel | spieceasi
    emit:
        // has `publishDir` -> ${params.output_dir}/${task.process}/${id}
        spieceasi.out
}
