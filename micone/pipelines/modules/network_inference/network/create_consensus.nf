include { getHierarchy } from '../../../functions/functions.nf'

process create_consensus {
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
        method = params.network_inference.network['create_consensus']['method']
        parameter = params.network_inference.network['create_consensus']['parameter']
        pvalue_filter = params.network_inference.network['create_consensus']['pvalue_filter']
        interaction_filter = params.network_inference.network['create_consensus']['interaction_filter']
        template 'network_inference/network/create_consensus.py'
}
