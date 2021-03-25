include { create_seqtable } from './create_seqtable.nf'
include { remove_bimera } from './remove_bimera.nf'
include { hashing3 } from './../denoise_cluster/hashing3.nf'


workflow remove_bimera_workflow {
    take:
        // tuple val(id), file(otutable_file), file(repseqs_file)
        input_channel
    main:
        input_channel \
            | create_seqtable \
            | remove_bimera \
            | hashing3
    emit:
        // has `publishDir` -> ${params.output_dir}/${id}
        hashing3.out
}
