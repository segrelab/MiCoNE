// Step2: de_novo OTU picking
process de_novo {
    lable 'qiime1'
    tag "${meta.id}"
    input:
        tuple val(meta), file(fasta_file)
    output:
        tuple val(meta), file('unhashed_otu_table.biom'), file('unhashed_rep_seqs.fasta'), file('log*.txt')
    when:
        "de_novo" in params.denoise_cluster.otu_assignment['selection']
    script:
        meta.denoise_cluster = "de_novo"
        ncpus = params.denoise_cluster.otu_assignment['de_novo']['ncpus']
        parameters = params.denoise_cluster.otu_assignment['de_novo']['parameters']
        parallel_option = ncpus > 1 ? "-a -O ${ncpus}" : ''
        template 'denoise_cluster/otu_assignment/pick_de_novo_otus.sh'
}
