include { getHierarchy } from ='../../../functions/functions.nf'

process make_network_without_pvalue {
    label 'micone'
    tag "${meta.id}"
    publishDir "${params.output_dir}/${f[0]}/${f[1]}/${f[2]}/${meta.id}",
        mode: 'copy',
        overwrite: true
    input:
        tuple val(meta), file(corr_file), file(obs_metadata), file(sample_metadata), file(children_map)
    output:
        tuple val(meta), file('*_network.json')
    script:
        String task_process = "${task.process}"
        f = getHierarchy(task_process)
        metadata = params.network_inference.network['make_network_without_pvalue']['metadata']
        interaction_threshold = params.network_inference.network['make_network_without_pvalue']['interaction_threshold']
        template 'network_inference/network/make_network_without_pvalue.py'
}
