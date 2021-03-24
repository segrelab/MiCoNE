process make_network {
    tag "$id"
    publishDir "${output_dir}/${datatuple}", mode: 'copy', overwrite: true
    input:
    tuple val(id), val(datatuple), val(level), file(corr_file), file(pval_file), file(obsdata_file), file(childrenmap_file)
    output:
    tuple val(id), file('*_network.json')
    script:
    template 'network_inference/network/make_network.py'
}
