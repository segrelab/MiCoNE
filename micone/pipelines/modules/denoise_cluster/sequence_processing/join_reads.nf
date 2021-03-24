// TODO: Move this to workflows
// Step0: Join sequence and barcode channels
chnl_sequences
    .join(chnl_barcodes)
    .tuple { chnl_sequence_join }

// Step1: Join reads
process  join_reads {
    tag "${id}"
    publishDir "${output_dir}/${id}", saveAs: { filename -> filename.split("/")[1] }, mode: 'copy', overwrite: true
    input:
    tuple val(id), val(sequence_files), file(barcode_file)
    output:
    tuple val(id), file('joined_reads/*_reads.fastq.gz'), file('joined_reads/*_barcodes.fastq.gz')
    script:
    template 'denoise_cluster/sequence_processing/join_reads.sh'
}
