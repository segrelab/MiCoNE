include { getHierarchy } from '../../../functions/functions.nf'

// Step3: Export files
process export_files {
    label 'qiime2'
    tag "${meta.id}"
    publishDir "${params.output_dir}/${f[0]}/${f[1]}/filtered_output/${meta.denoise_cluster}/${meta.id}",
        mode: 'copy',
        overwrite: true
    input:
        tuple val(meta), file(otutable_nonchimeric), file(repseqs_nonchimeric), file(samplemetadata_files)
    output:
        tuple val(meta), file("otu_table.biom"), file("rep_seqs.fasta"), file(samplemetadata_files)
    script:
        String task_process = "${task.process}"
        f = getHierarchy(task_process)
        template 'denoise_cluster/chimera_checking/export_files.sh'
}
