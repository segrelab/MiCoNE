process export_gml {
    label 'flashweave'
    tag "${id}"
    publishDir "${params.output_dir}/${task.process}/${id}", mode: 'copy', overwrite: true
    input:
        tuple val(id), val(datatuple), file(otu_file), file(network_file)
    output:
        tuple val(id), file('*_corr.tsv')
    script:
        template 'network_inference/direct/export_gml.py'
}
