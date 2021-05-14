// Import the sequences
process import_sequences {
    label 'qiime2'
    tag "${id}"
    input:
        tuple val(id), file(sequence_file), file(barcode_file)
    output:
        tuple val(id), file('*_sequences.qza')
    script:
        template 'denoise_cluster/sequence_processing/import_sequences.sh'
}

