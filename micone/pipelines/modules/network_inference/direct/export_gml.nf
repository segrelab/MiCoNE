process export_gml {
    tag "${id}"
    publishDir "${output_dir}/${datatuple}", mode: 'copy', overwrite: true
    input:
    tuple val(id), val(datatuple), file(otu_file), file(network_file)
    output:
    tuple val(id), file('*_corr.tsv')
    script:
    template 'network_inference/direct/export_gml.py'
}
