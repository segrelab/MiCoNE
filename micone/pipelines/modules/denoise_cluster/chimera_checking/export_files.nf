// Step3: Export files
process export_files {
    label 'qiime2'
    tag "${id}"
    publishDir "${params.output_dir}/${id}", mode: 'copy', overwrite: true
    input:
        tuple val(id), file(otutable_nonchimeric), file(repseqs_nonchimeric)
    output:
        tuple val(id), file("otu_table.biom"), file("rep_seqs.fasta")
    script:
        template 'denoise_cluster/chimera_checking/export_files.sh'
}
