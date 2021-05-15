// Step2: open reference OTU picking
process open_reference {
    label 'qiime1'
    tag "${meta.id}"
    input:
        tuple val(meta), file(fasta_file)
    output:
        tuple val(meta), file('unhashed_otu_table.biom'), file('unhashed_rep_seqs.fasta'), file('log*.txt')
    script:
        ncpus = params.denoise_cluster.denoise_cluster['open_reference']['ncpus']
        parameters = params.denoise_cluster.denoise_cluster['open_reference']['parameters']
        reference_sequences = params.denoise_cluster.denoise_cluster['open_reference']['reference_sequences']
        picking_method = params.denoise_cluster.denoise_cluster['open_reference']['picking_method']
        parallel_option = ncpus > 1 ? "-a -O ${ncpus}" : ''
        template 'denoise_cluster/denoise_cluster/pick_open_reference_otus.sh'
}
