// Import the sequences to qiime2 artifacts
process import_sequences {
    label 'qiime2'
    tag "${id}"
    input:
        tuple val(id), file(sequence_files), file(manifest_file)
    output:
        tuple val(id), file('sequence_folder/*.qza')
    script:
        template 'denoise_cluster/sequence_processing/import_sequences.py'
}

