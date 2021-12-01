include { getHierarchy } from '../../../functions/functions.nf'

process merge_pvalues {
    label 'micone'
    publishDir "${params.output_dir}/${f[0]}/network/${f[1]}",
        mode: 'copy',
        overwrite: true
    input:
        file('*_network.json')
    output:
        file('merged/*.json')
    script:
        String task_process = "${task.process}"
        f = getHierarchy(task_process)
        id_field = params.network_inference.network['merge_pvalues']['id_field']
        template 'network_inference/network/merge_pvalues.py'
}
