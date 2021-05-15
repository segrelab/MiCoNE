process sparcc {
    label 'sparcc'
    tag "${id}"
    publishDir "${params.output_dir}/${task.process}/${id}", mode: 'copy', overwrite: true
    input:
        // tuple val(id), val(datatuple), val(level), file(otu_file)
        tuple val(id), file(otu_file), file(sample_metadata)
    output:
        tuple val(id), file('*_corr.tsv')
    when:
        'sparcc' in params.ni_tools
    script:
        template 'network_inference/correlation/sparcc.sh'
}
