include { deblur } from './deblur.nf'
include { hashing3 } from './hashing3.nf'


workflow deblur_workflow {
    take:
        // tuple val(id), file(sequence_files), file(manifest_file)
        input_channel
    main:
        input_channel \
            | deblur \
            | hashing3
    emit:
        // has `publishDir` -> ${params.output_dir}/${task.process}/${id}
        hashing3.out
}
