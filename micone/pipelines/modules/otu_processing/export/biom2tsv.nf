include { getHierarchy; updateMeta } from '../../../functions/functions.nf'

process biom2tsv {
    label 'micone'
    tag "${meta.id}"
    publishDir "${params.output_dir}/${f[0]}/export/${f[1]}/${directory}/${meta.id}",
        mode: 'copy',
        overwrite: true
    input:
        tuple val(meta), file(otu_file), file(children_file)
    output:
        tuple val(meta), file("*_otu.tsv"), file("*_obs_metadata.csv"), file("*_sample_metadata.tsv"), file(children_file)
    script:
        String task_process = "${task.process}"
        f = getHierarchy(task_process)
    directory = "${meta.denoise_cluster}-${meta.chimera_checking}-${meta.tax_assignment}-${meta.otu_processing}"
        template 'otu_processing/export/biom2tsv.py'
}
