include { updateMeta } from '../../../functions/functions.nf'

// Step2: de_novo OTU picking
process de_novo {
    label 'qiime1'
    tag "${new_meta.id}"
    input:
        tuple val(meta), file(fasta_file), file(samplemetadata_files)
    output:
        tuple val(new_meta), file('*_unhashed_otu_table.biom'), file('*_unhashed_rep_seqs.fasta'), file('log*.txt'), file('*_sample_metadata.tsv')
    when:
        "de_novo" in params.denoise_cluster.otu_assignment['selection']
    script:
        new_meta = updateMeta(meta)
        new_meta.denoise_cluster = 'de_novo'
        ncpus = params.denoise_cluster.otu_assignment['de_novo']['ncpus']
        parameters = params.denoise_cluster.otu_assignment['de_novo']['parameters']
        parallel_option = ncpus > 1 ? "-a -O ${ncpus}" : ''
        template 'denoise_cluster/otu_assignment/pick_de_novo_otus.sh'
}
