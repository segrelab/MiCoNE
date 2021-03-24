process calculate_pvalues {
    tag "${id}"
    publishDir "${output_dir}/${datatuple}", mode: 'copy', overwrite: true
    input:
    tuple val(id), val(datatuple), val(level), file(otu_file), file(corr_file), file(corr_bootstrap)
    output:
    tuple val(id), file('*_pval.tsv')
    script:
    template 'network_inference/bootstrap/calculate_pvalues.sh'
}

