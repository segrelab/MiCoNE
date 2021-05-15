// Step2: Closed reference OTU picking
process closed_reference {
    label 'qiime1'
    tag "${meta.id}"
    input:
        tuple val(meta), file(fasta_file)
    output:
        tuple val(meta), file('unhashed_otu_table.biom'), file('unhashed_rep_seqs.fasta'), file('log*.txt')
    script:
        ncpus = params.denoise_cluster.denoise_cluster['closed_reference']['ncpus']
        parameters = params.denoise_cluster.denoise_cluster['closed_reference']['parameters']
        reference_sequences = params.denoise_cluster.denoise_cluster['closed_reference']['reference_sequences']
        parallel_option = ncpus > 1 ? "-a -O ${ncpus}" : ''
        template 'denoise_cluster/denoise_cluster/pick_closed_reference_otus.sh'
}
