// Step2: Closed reference OTU picking
process closed_reference {
    label 'qiime1'
    tag "${id}"
    input:
        tuple val(id), file(fasta_file)
    output:
        tuple val(id), file('unhashed_otu_table.biom'), file('unhashed_rep_seqs.fasta'), file('log*.txt')
    script:
        def parallel_option = ncpus > 1 ? "-a -O ${ncpus}" : ''
        template 'denoise_cluster/denoise_cluster/pick_closed_reference_otus.sh'
}