// Step1: Convert fastq to fasta and merge
process fastq2fasta {
    tag "${id}"
    input:
    tuple val(id), file(sequence_files), file(manifest_file)
    output:
    tuple val(id), file("${id}.fasta")
    script:
    template 'denoise_cluster/denoise_cluster/fastq2fasta.py'
}
