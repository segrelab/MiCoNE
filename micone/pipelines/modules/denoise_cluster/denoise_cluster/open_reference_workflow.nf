include { fastq2fasta } from './fastq2fasta.nf'
include { open_reference } from './open_reference.nf'
include { hashing2 } from './hashing2.nf'


workflow de_novo_workflow {
    take:
        // tuple val(id), file(sequence_files), file(manifest_file)
        input_channel
    main:
        input_channel \
            | fastq2fasta \
            | open_reference \
            | hashing2
    emit:
        // has `publishDir` -> ${params.output_dir}/${task.process}/${id}
        hashing2.out
}
