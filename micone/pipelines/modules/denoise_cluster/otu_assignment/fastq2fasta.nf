// Convert fastq to fasta and merge
process fastq2fasta {
    label 'qiime2'
    tag "${meta.id}-${meta.run}"
    input:
        tuple val(meta), file(sequence_files), file(manifest_file), file(sequence_metadata), file(samplemetadata_files)
    output:
        tuple val(meta), file("*.fasta"), file(samplemetadata_files)
    script:
        template 'denoise_cluster/otu_assignment/fastq2fasta.py'
}
