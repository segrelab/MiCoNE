include { getHierarchy } from ='../../../functions/functions.nf'

process spieceasi {
    label 'spieceasi'
    tag "${meta.id}"
    publishDir "${params.output_dir}/${f[0]}/${f[1]}/${f[2]}/${meta.id}",
        mode: 'copy',
        overwrite: true
    input:
        tuple val(meta), file(otu_file), file(obs_metadata), file(sample_metadata), file(children_map)
    output:
        tuple val(meta), file('*_corr.tsv'), file(obs_metadata), file(sample_metadata), file(children_map)
    when:
        'spieceasi' in params.network_inference.correlation['selection']
    script:
        meta.network_inference = 'spieceasi'
        String task_process = "${task.process}"
        f = getHierarchy(task_process)
        method = params.network_inference.direct['spieceasi']['method']
        ncpus = params.network_inference.direct['spieceasi']['ncpus']
        nreps = params.network_inference.direct['spieceasi']['nreps']
        nlambda = params.network_inference.direct['spieceasi']['nlambda']
        lambda_min_ratio = params.network_inference.direct['spieceasi']['lambda_min_ratio']
        template 'network_inference/direct/spieceasi.R'
}
