include { getHierarchy } from '../../../functions/functions.nf'

process normalize {
    label 'micone'
    tag "${meta.id}"
    publishDir "${params.output_dir}/${f[0]}/transform/${f[1]}/${directory}/${meta.id}",
        mode: 'copy',
        overwrite: true
    input:
        tuple val(meta), file(otu_file)
    output:
        tuple val(meta), file("*_normalized.biom")
    script:
        String task_process = "${task.process}"
        f = getHierarchy(task_process)
        directory = "${meta.denoise_cluster}-${meta.chimera_checking}-${meta.tax_assignment}"
        axis = params.otu_processing.transform['normalize']['axis']
        count_thres = params.otu_processing.transform['normalize']['count_thres']
        prevalence_thres = params.otu_processing.transform['normalize']['prevalence_thres']
        abundance_thres = params.otu_processing.transform['normalize']['abundance_thres']
        rm_sparse_obs = params.otu_processing.transform['normalize']['rm_sparse_obs']
        rm_sparse_samples = params.otu_processing.transform['normalize']['rm_sparse_samples']
        template 'otu_processing/transform/normalize.py'
}
