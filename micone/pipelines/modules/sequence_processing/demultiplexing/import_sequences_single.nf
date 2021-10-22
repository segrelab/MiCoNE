// Import the sequences
process import_sequences_single {
    label 'qiime2'
    tag "${meta.id}-${meta.run}"
    input:
        tuple val(meta), file(sequence_file), file(barcode_file), file(mapping_file)
    output:
        tuple val(meta), file('*_sequences.qza'), file(mapping_file)
    script:
        template 'sequence_processing/demultiplexing/import_sequences_single.sh'
}
