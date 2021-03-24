process flashweave {
    tag "${id}"
    input:
    tuple val(id), val(datatuple), val(level), file(otu_file)
    output:
    tuple val(id), val(datatuple), file(otu_file), file('*_network.gml')
    script:
    template 'network_inference/direct/flashweave.jl'
}
