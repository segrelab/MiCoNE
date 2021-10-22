// Import the sequences to qiime2 artifacts
process import_sequences_paired {
    label 'qiime2'
    tag "${meta.id}-${meta.run}"
    input:
        tuple val(meta), file(sequence_files), file(manifest_file)
    output:
        tuple val(meta), file('*_sequences.qza')
    script:
        template 'sequence_processing/trimming/import_sequences_paired.py'
}

