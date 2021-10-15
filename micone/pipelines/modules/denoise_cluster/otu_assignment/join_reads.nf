include { getHierarchy } from '../../../functions/functions.nf'

// Join reads
process join_reads {
    label 'qiime2'
    tag "${meta.id}"
    publishDir "${params.output_dir}/${f[0]}/${f[1]}/${f[2]}/${meta.id}",
        saveAs: { filename -> filename.split("/")[1] }
        mode: 'copy',
        overwrite: true
    input:
        tuple val(meta), file(sequence_files), file(manifest_file)
    output:
        tuple val(meta), file('joined_reads/*.fastq.gz'), file('joined_reads/MANIFEST')
    script:
        String task_process = "${task.process}"
        f = getHierarchy(task_process)
        template 'denoise_cluster/otu_assignment/join_reads.sh'
}
