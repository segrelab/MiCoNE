process resample {
    label 'sparcc'
    tag "${meta.id}"
    input:
        tuple val(meta), file(otu_file), file(obs_metadata), file(sample_metadata), file(children_map)
    output:
        tuple val(meta), file(otu_file), file('bootstraps/*.boot.temp'), file(obsmeta_file), file(samplemeta_file), file(children_file)
    script:
        ncpus = params.network_inference.bootstrap['resample']['ncpus']
        bootstraps = params.network_inference.bootstrap['resample']['bootstraps']
        template 'network_inference/bootstrap/resample.sh'
}
