include { updateMeta } from '../../../functions/functions.nf'

// Step2: open reference OTU picking
process open_reference {
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
        "open_reference" in params.denoise_cluster.otu_assignment['selection']
    script:
        new_meta = updateMeta(meta)
        new_meta.denoise_cluster = 'open_reference'
        reference_sequences = params.denoise_cluster.otu_assignment['open_reference']['reference_sequences']
        percent_identity = params.denoise_cluster.otu_assignment['open_reference']['percent_identity']
        strand = params.denoise_cluster.otu_assignment['open_reference']['strand']
        ncpus = params.denoise_cluster.otu_assignment['open_reference']['ncpus']
        template 'denoise_cluster/otu_assignment/cluster_open_reference.sh'
}
