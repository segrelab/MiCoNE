// Join reads
process join_reads {
    label 'qiime1'
    tag "${meta.id}"
    publishDir "${params.output_dir}/${task.process}/${meta.id}", saveAs: { filename -> filename.split("/")[1] }, mode: 'copy', overwrite: true
    input:
        tuple val(meta), val(sequence_files), file(barcode_file)
    output:
        tuple val(meta), file('joined_reads/*_reads.fastq.gz'), file('joined_reads/*_barcodes.fastq.gz')
    script:
        def min_overlap = params.denoise_cluster.sequence_processing['join_reads']['min_overlap']
        def perc_max_diff = params.denoise_cluster.sequence_processing['join_reads']['perc_max_diff']
        template 'denoise_cluster/sequence_processing/join_reads.sh'
}
