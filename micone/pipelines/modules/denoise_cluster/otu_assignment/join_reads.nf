include { getHierarchy } from '../../../functions/functions.nf'

// Join reads
process join_reads {
    label 'qiime2'
    tag "${meta.id}-${meta.run}"
    publishDir "${params.output_dir}/${f[0]}/${f[1]}/${f[2]}/${meta.id}-${meta.run}",
        saveAs: { filename -> filename.split("/")[-1] },
        mode: 'copy',
        overwrite: true
    input:
        tuple val(meta), file(sequence_files), file(manifest_file), file(sequence_metadata), file(samplemetadata_files)
    output:
        tuple val(meta), file('joined_reads/*.fastq.gz'), file('joined_reads/MANIFEST'), file('joined_reads/metadata.yml'), file(samplemetadata_files)
    script:
        String task_process = "${task.process}"
        f = getHierarchy(task_process)
        template 'denoise_cluster/otu_assignment/join_reads.sh'
}
