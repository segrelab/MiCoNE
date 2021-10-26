include { import_sequences_paired } from './import_sequences_paired.nf'
include { demultiplexing_illumina_paired } from './demultiplexing_illumina_paired.nf'
include { export_sequences } from './export_sequences.nf'


workflow demultiplexing_paired_workflow {
    take:
        // tuple val(meta), file(forward_file), file(reverse_file), file(barcode_file), file(mapping_file)
        input_channel
    main:
        input_channel \
            | import_sequences_paired \
            | demultiplexing_illumina_paired \
            | export_sequences
    emit:
        // export_sequences and join_reads has publishDir
        // tuple val(meta), file('demux_seqs/*.fastq.gz'), file('demux_seqs/MANIFEST'), file('demux_seqs/metadata.yml')
        export_sequences.out
}
