include { import_sequences_sh } from './import_sequences_sh.nf'
include { demultiplexing_illumina } from './demultiplex_illumina.nf'
include { export_sequences } from './export_sequences.nf'


workflow demultiplexing_illumina_workflow {
    take:
        // tuple val(meta), file(sequence_file), file(barcode_file), file(mapping_file)
        input_channel
    main:
        input_channel \
            | import_sequences_sh \
            | demultiplexing_illumina \
            | export_sequences \
            | join_reads
    // TODO: Connect `join_reads` properly
    emit:
        // export_sequences and join_reads has publishDir
        // tuple val(meta), file('joined_reads/*_reads.fastq.gz'), file('joined_reads/*_barcodes.fastq.gz')
        join_reads.out
}
