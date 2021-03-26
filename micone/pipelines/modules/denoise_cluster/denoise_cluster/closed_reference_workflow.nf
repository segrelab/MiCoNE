include { fastq2fasta } from './fastq2fasta.nf'
include { closed_reference } from './closed_reference.nf'
include { hashing2 } from './hashing2.nf'


workflow closed_reference_workflow {
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
