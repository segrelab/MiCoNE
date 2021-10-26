include { import_sequences_single } from './import_sequences_single.nf'
include { demultiplexing_illumina_single } from './demultiplexing_illumina_single.nf'
include { export_sequences } from './export_sequences.nf'


workflow demultiplexing_single_workflow {
    take:
        // tuple val(meta), file(sequence_file), file(barcode_file), file(mapping_file)
        input_channel
    main:
        input_channel \
            | import_sequences_single \
            | demultiplexing_illumina_single \
            | export_sequences
    emit:
        // export_sequences and join_reads has publishDir
        // tuple val(meta), file('demux_seqs/*.fastq.gz'), file('demux_seqs/MANIFEST'), file('demux_seqs/metadata.yml')
        export_sequences.out
}
