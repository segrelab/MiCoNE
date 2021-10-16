// Step1: Import files as artifacts
process import_files {
    label 'qiime2'
    tag "${meta.id}"
    input:
        tuple val(meta), file(otutable_file), file(repseqs_file), file(samplemetadata_files)
    output:
        tuple val(meta), file("otu_table.qza"), file("rep_seqs.qza"), file(samplemetadata_files)
    script:
        template 'denoise_cluster/chimera_checking/import_files.sh'
}
