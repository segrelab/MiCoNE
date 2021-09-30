include { getHierarchy; updateMeta } from '../../../functions/functions.nf'

process spieceasi {
    label 'spieceasi'
    tag "${new_meta.id}"
    publishDir "${params.output_dir}/${f[0]}/${f[1]}/${f[2]}/${directory}/${new_meta.id}",
        mode: 'copy',
        overwrite: true
    input:
        tuple val(meta), file(otu_file), file(obs_metadata), file(sample_metadata), file(children_map)
    output:
        tuple val(new_meta), file('*_corr.tsv'), file(obs_metadata), file(sample_metadata), file(children_map)
    when:
        'spieceasi' in params.network_inference.direct['selection']
    script:
        new_meta = updateMeta(meta)
        new_meta.network_inference = 'spieceasi'
        String task_process = "${task.process}"
        f = getHierarchy(task_process)
        directory = "${meta.denoise_cluster}-${meta.chimera_checking}-${meta.tax_assignment}-${meta.tax_level}"
        method = params.network_inference.direct['spieceasi']['method']
        ncpus = params.network_inference.direct['spieceasi']['ncpus']
        nreps = params.network_inference.direct['spieceasi']['nreps']
        nlambda = params.network_inference.direct['spieceasi']['nlambda']
        lambda_min_ratio = params.network_inference.direct['spieceasi']['lambda_min_ratio']
        template 'network_inference/direct/spieceasi.R'
}
