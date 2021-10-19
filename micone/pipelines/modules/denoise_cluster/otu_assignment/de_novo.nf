include { updateMeta } from '../../../functions/functions.nf'

// Step2: de_novo OTU picking
process de_novo {
    label 'qiime2'
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
        percent_identity = params.denoise_cluster.otu_assignment['de_novo']['percent_identity']
        ncpus = params.denoise_cluster.otu_assignment['de_novo']['ncpus']
        template 'denoise_cluster/otu_assignment/cluster_de_novo.sh'
}
