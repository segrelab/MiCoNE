process resample {
    label 'sparcc'
    tag "${meta.id}"
    input:
        tuple val(meta), file(otu_file), file(obs_metadata), file(sample_metadata), file(children_map)
    output:
        tuple val(meta), file(otu_file), file('bootstraps/*_otu.boot'), file(obs_metadata), file(sample_metadata), file(children_map)
    script:
        ncpus = params.network_inference.bootstrap['resample']['ncpus']
        bootstraps = params.network_inference.bootstrap['resample']['bootstraps']
        template 'network_inference/bootstrap/resample.sh'
}
