// Step1: Import files as artifacts
process import_files {
    label 'qiime2'
    tag "${id}"
    input:
        tuple val(id), file(otu_table), file(rep_seqs)
    output:
        tuple val(id), file("otu_table.qza"), file("rep_seqs.qza")
    script:
        template 'denoise_cluster/chimera_checking/import_files.sh'
}
