include { updateMeta } from '../../../functions/functions.nf'

// Step2: de_novo OTU picking
process de_novo {
    label 'qiime2'
    tag "${new_meta.id}-${new_meta.run}"
    input:
        tuple val(meta), file(fasta_file), file(samplemetadata_files)
    output:
        val(new_meta), emit: meta_channel
        path('*_unhashed_otu_table.biom'), emit: otu_channel
        path('*_unhashed_rep_seqs.fasta'), emit: repseq_channel
        path('*_sample_metadata.tsv'), emit: samplemetadata_channel
    when:
        "de_novo" in params.denoise_cluster.otu_assignment['selection']
    script:
        new_meta = updateMeta(meta)
        new_meta.denoise_cluster = 'de_novo'
        percent_identity = params.denoise_cluster.otu_assignment['de_novo']['percent_identity']
        ncpus = params.denoise_cluster.otu_assignment['de_novo']['ncpus']
        template 'denoise_cluster/otu_assignment/cluster_de_novo.sh'
}
