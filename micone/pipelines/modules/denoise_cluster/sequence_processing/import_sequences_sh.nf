// Import the sequences
process import_sequences {
    label 'qiime2'
    tag "${meta.id}"
    input:
        tuple val(meta), file(sequence_file), file(barcode_file), file(mapping_file)
    output:
        tuple val(meta), file('*_sequences.qza'), file(mapping_file)
    script:
        template 'denoise_cluster/sequence_processing/import_sequences.sh'
}

