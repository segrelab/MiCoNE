// Join reads
process join_reads {
    label 'qiime1'
    tag "${id}"
    publishDir "${params.output_dir}/${task.process}/${id}", saveAs: { filename -> filename.split("/")[1] }, mode: 'copy', overwrite: true
    input:
        tuple val(id), val(sequence_files), file(barcode_file)
    output:
        tuple val(id), file('joined_reads/*_reads.fastq.gz'), file('joined_reads/*_barcodes.fastq.gz')
    script:
        template 'denoise_cluster/sequence_processing/join_reads.sh'
}
