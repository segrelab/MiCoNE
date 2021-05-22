process mldm {
    label 'mldm'
    tag "${meta.id}"
    publishDir "${params.output_dir}/${f[0]}/${f[1]}/${f[2]}/${meta.id}",
        mode: 'copy',
        overwrite: true
    input:
        tuple val(meta), file(otu_file), file(obs_metadata), file(sample_metadata), file(children_map)
    output:
        tuple val(meta), file('*_corr.tsv'), file(obs_metadata), file(sample_metadata), file(children_map)
    when:
        'mldm' in params.network_inference.correlation['selection']
    script:
        String task_process = "${task.process}"
        f = getHierarchy(task_process)
        Z_mean = params.network_inference.direct['mldm']['Z_mean']
        max_iteration = params.network_inference.direct['mldm']['max_iteration']
        template 'network_inference/direct/mldm.R'
}
