include { getHierarchy } from '../../../functions/functions.nf'

process create_consensus {
    label 'micone'
    publishDir "${params.output_dir}/${f[0]}/network/${f[1]}",
        mode: 'copy',
        overwrite: true
    input:
        file('*_network.json')
    output:
        file('consensus/*.json')
    script:
        String task_process = "${task.process}"
        f = getHierarchy(task_process)
        method = params.network_inference.network['create_consensus']['method']
        parameter = params.network_inference.network['create_consensus']['parameter']
        pvalue_filter = params.network_inference.network['create_consensus']['pvalue_filter']
        interaction_filter = params.network_inference.network['create_consensus']['interaction_filter']
        id_field = params.network_inference.network['create_consensus']['id_field']
        template 'network_inference/network/create_consensus.py'
}
