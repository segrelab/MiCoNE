// Convert fastq to fasta and merge
process fastq2fasta {
    label 'qiime1'
    tag "${meta.id}"
    input:
        tuple val(meta), file(sequence_files), file(manifest_file)
    output:
        tuple val(meta), file("*.fasta")
    script:
        ncpus = params.denoise_cluster.denoise_cluster['closed_reference']['ncpus']
        template 'denoise_cluster/denoise_cluster/fastq2fasta.py'
}
