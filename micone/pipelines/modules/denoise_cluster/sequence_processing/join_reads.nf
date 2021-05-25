include { getHierarchy } from '../../../functions/functions.nf'

// Join reads
process join_reads {
    label 'qiime1'
    tag "${meta.id}"
    publishDir "${params.output_dir}/${f[0]}/${f[1]}/${f[2]}/${meta.id}",
        saveAs: { filename -> filename.split("/")[1] },
        mode: 'copy',
        overwrite: true
    input:
        tuple val(meta), val(sequence_files), file(barcode_file)
    output:
        tuple val(meta), file('joined_reads/*_reads.fastq.gz'), file('joined_reads/*_barcodes.fastq.gz')
    script:
        String task_process = "${task.process}"
        f = getHierarchy(task_process)
        min_overlap = params.denoise_cluster.sequence_processing['join_reads']['min_overlap']
        perc_max_diff = params.denoise_cluster.sequence_processing['join_reads']['perc_max_diff']
        template 'denoise_cluster/sequence_processing/join_reads.sh'
}
