// Step2: Remove chimeras using removeBimeraDenovo
process remove_chimeras {
    tag "${id}"
    input:
    tuple val(id), file(seqtable_file)
    output:
    tuple val(id), file("unhashed_otu_table.biom"), file("unhashed_rep_seqs.fasta")
    script:
    template 'denoise_cluster/chimera_checking/remove_chimeras.R'
}
