// Step1: Import files as artifacts
process import_files {
    label 'qiime2'
    tag "${meta.id}"
    input:
        tuple val(meta), file(otutable_file), file(repseqs_file)
    output:
        tuple val(meta), file("otu_table.qza"), file("rep_seqs.qza")
    script:
        template 'denoise_cluster/chimera_checking/import_files.sh'
}
