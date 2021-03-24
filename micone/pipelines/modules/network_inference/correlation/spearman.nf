process spearman {
    tag "${id}"
    publishDir "${output_dir}/${datatuple}", mode: 'copy', overwrite: true
    input:
    tuple val(id), val(datatuple), val(level), file(otu_file)
    output:
    tuple val(id), file('*_corr.tsv')
    script:
    template 'network_inference/correlation/spearman.py'
}
