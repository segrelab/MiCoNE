include { getHierarchy; updateMeta } from '../../../functions/functions.nf'

process harmonies {
    label 'harmonies'
    tag "${new_meta.id}"
    publishDir "${params.output_dir}/${f[0]}/${f[1]}/${f[2]}/${directory}/${new_meta.id}",
        mode: 'copy',
        overwrite: true
    input:
        tuple val(meta), file(otu_file), file(obs_metadata), file(sample_metadata), file(children_map)
    output:
        tuple val(new_meta), file('*_corr.tsv'), file(obs_metadata), file(sample_metadata), file(children_map)
    when:
        'harmonies' in params.network_inference.direct['selection']
    script:
        new_meta = updateMeta(meta)
        new_meta.network_inference = 'harmonies'
        String task_process = "${task.process}"
        f = getHierarchy(task_process)
        directory = "${meta.denoise_cluster}-${meta.chimera_checking}-${meta.tax_assignment}-${meta.tax_level}"
        iterations = params.network_inference.direct['harmonies']['iterations']
        sparsity_cutoff = params.network_inference.direct['harmonies']['sparsity_cutoff']
        template 'network_inference/direct/harmonies.R'
}
