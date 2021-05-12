process flashweave {
    label 'flashweave'
    tag "${id}"
    publishDir "${params.output_dir}/${task.process}/${id}", mode: 'copy', overwrite: true
    input:
        tuple val(id), val(datatuple), val(level), file(otu_file)
    output:
        tuple val(id), val(datatuple), file(otu_file), file('*_network.gml')
    script:
        template 'network_inference/direct/flashweave.jl'
}
