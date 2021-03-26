include { dada2 } from './dada2.nf'
include { make_biom_repseqs } from './make_biom_repseqs.nf'
include { hashing3 } from './hashing3.nf'


workflow dada2_workflow {
    take:
        // tuple val(id), file(sequence_files), file(manifest_file)
        input_channel
    main:
        input_channel \
            | dada2 \
            | make_biom_repseqs \
            | hashing3
    emit:
        // has `publishDir` -> ${params.output_dir}/${task.process}/${id}
        hashing3.out
}
