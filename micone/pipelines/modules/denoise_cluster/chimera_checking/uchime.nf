// Remove chimeras using vserach uchime-denovo
process uchime {
    label 'qiime2'
    tag "${meta.id}"
    input:
        tuple val(meta), file(otutable_artifact), file(repseqs_artifact)
    output:
        tuple val(meta), file("otu_table_nonchimeric.qza"), file("rep_seqs_nonchimeric.qza")
    script:
        template 'denoise_cluster/chimera_checking/remove_chimeras.sh'
}
