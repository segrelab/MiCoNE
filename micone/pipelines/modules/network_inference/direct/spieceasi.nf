process spieceasi {
    label 'spieceasi'
    tag "${id}"
    publishDir "${params.output_dir}/${task.process}/${id}", mode: 'copy', overwrite: true
    input:
        tuple val(id), val(datatuple), val(level), file(otu_file)
    output:
        tuple val(id), file('*_corr.tsv')
    script:
        template 'network_inference/direct/spieceasi.R'
}
