// TODO: FIXME: This needs to take in two channels and the join them by id
process pvalues {
    label 'sparcc'
    tag "${id}"
    publishDir "${params.output_dir}/${task.process}/${id}", mode: 'copy', overwrite: true
    input:
        tuple val(id), val(datatuple), val(level), file(otu_file), file(corr_file), file(corr_bootstrap)
    output:
        tuple val(id), file('*_pval.tsv')
    script:
        template 'network_inference/bootstrap/calculate_pvalues.sh'
}
