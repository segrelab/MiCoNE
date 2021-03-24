// TODO: Move this to workflows
// Step1: Create lists of [id, sequence, barcode, mapping] for each sample
chnl_sequences
    .join(chnl_barcodes)
    .tuple { chnl_sequence_import }

// Step2: Import the sequences
process import_sequences {
    tag "${id}"
    input:
    tuple val(id), file(sequence_file), file(barcode_file)
    output:
    tuple val(id), file('*_sequences.qza')
    script:
    template 'denoise_cluster/sequence_processing/import_sequences.sh'
}

