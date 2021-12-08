include { getHierarchy; updateMeta } from '../../../functions/functions.nf'

process mldm {
    label 'mldm'
    tag "${new_meta.id}"
    publishDir "${params.output_dir}/${f[0]}/${f[1]}/${f[2]}/${directory}/${new_meta.id}",
        mode: 'copy',
        overwrite: true
    input:
        tuple val(meta), file(otu_file), file(obs_metadata), file(sample_metadata), file(children_map)
    output:
        tuple val(new_meta), file('*_corr.tsv'), file(obs_metadata), file(sample_metadata), file(children_map)
    when:
        'mldm' in params.network_inference.direct['selection']
    script:
        new_meta = updateMeta(meta)
        new_meta.network_inference = 'mldm'
        String task_process = "${task.process}"
        f = getHierarchy(task_process)
        directory = "${new_meta.denoise_cluster}-${new_meta.chimera_checking}-${new_meta.tax_assignment}-${new_meta.otu_processing}"
        Z_mean = params.network_inference.direct['mldm']['Z_mean']
        max_iteration = params.network_inference.direct['mldm']['max_iteration']
        template 'network_inference/direct/mldm.R'
}
