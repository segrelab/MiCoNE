process resample {
    tag "${id}"
    input:
    tuple val(id), val(datatuple), val(level), file(otu_file)
    output:
    tuple val(id), val(datatuple), val(level), file('bootstraps/*.boot.temp')
    script:
    template 'network_inference/bootstrap/resample.sh'
}
