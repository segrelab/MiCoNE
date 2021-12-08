include { getHierarchy } from '../../../functions/functions.nf'

process make_network_with_pvalue {
    label 'micone'
    tag "${meta.id}"
    publishDir "${params.output_dir}/${f[0]}/network/${f[1]}/${directory}/${meta.id}",
        mode: 'copy',
        overwrite: true
    input:
        tuple val(meta), file(corr_file), file(pvalue_file), file(obs_metadata), file(sample_metadata), file(children_map)
    output:
        file('*_network.json')
    script:
        String task_process = "${task.process}"
        f = getHierarchy(task_process)
        directory = "${meta.denoise_cluster}-${meta.chimera_checking}-${meta.tax_assignment}-${meta.otu_processing}-${meta.network_inference}"
        metadata_file = params.network_inference.network['make_network_with_pvalue']['metadata_file']
        interaction_threshold = params.network_inference.network['make_network_with_pvalue']['interaction_threshold']
        pvalue_threshold = params.network_inference.network['make_network_with_pvalue']['pvalue_threshold']
        template 'network_inference/network/make_network_with_pvalue.py'
}
