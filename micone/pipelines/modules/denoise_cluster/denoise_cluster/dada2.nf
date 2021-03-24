// Step1: Denoise using dada2
process dada2 {
    tag "${id}"
    publishDir "${output_dir}/${id}", mode: 'copy', overwrite: true
    input:
    tuple val(id), file(sequence_files), file(manifest_file)
    output:
    tuple val(id), file("seq_table.tsv")
    script:
    template 'denoise_cluster/denoise_cluster/dada2.R'
}
