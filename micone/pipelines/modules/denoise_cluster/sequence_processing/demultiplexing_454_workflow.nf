include { validate_mapping } from './validate_mapping.nf'
include { demultiplexing_454 } from './demultiplexing_454.nf'


// TODO: Everything after this
// Having issues figuring out how to map inputs and channels and processes
workflow demultiplexing_454__workflow {
    take:
        // tuple val(id), file(sequence_files), file(manifest_file)
        input_channel
    main:
        input_channel \
            | fastq2fasta \
            | closed_reference \
            | hashing2
    emit:
        // has `publishDir` -> ${params.output_dir}/${task.process}/${id}
        hashing2.out
}
