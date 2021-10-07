include { getHierarchy } from '../../../functions/functions.nf'

process merge_pvalues {
    label 'micone'
    tag "${meta.id}"
    publishDir "${params.output_dir}/${f[0]}/network/${f[1]}/${directory}/${meta.id}",
        mode: 'copy',
        overwrite: true
    input:
        tuple val(meta), file('*_network.json')
    output:
        tuple val(meta), file('*_network.json')
    script:
        String task_process = "${task.process}"
        f = getHierarchy(task_process)
        directory = "${meta.denoise_cluster}-${meta.chimera_checking}-${meta.tax_assignment}-${meta.tax_level}-${meta.network_inference}"
        template 'network_inference/network/merge_pvalues.py'
}
