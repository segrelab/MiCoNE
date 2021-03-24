// Step2: Remove chimeras using vserach uchime-denovo
process remove_chimeras {
    tag "${id}"
    input:
    tuple val(id), file(otutable_artifact), file(repseqs_artifact)
    output:
    tuple val(id), file("otu_table_nonchimeric.qza"), file("rep_seqs_nonchimeric.qza")
    script:
    template 'denoise_cluster/chimera_checking/remove_chimeras.sh'
}

