// Step2: Make representative sequences and biom table
process make_biom_repseqs {
    label 'dada2'
    tag "${meta.id}-${meta.run}"
    input:
        tuple val(meta), file(seq_table_file), file(samplemetadata_files)
    output:
        val(meta), emit: meta_channel
        path('*_unhashed_otu_table.biom'), emit: otu_channel
        path('*_unhashed_rep_seqs.fasta'), emit: repseq_channel
        path('*_sample_metadata.tsv'), emit: samplemetadata_channel
    script:
        template 'denoise_cluster/otu_assignment/make_biom_repseqs.py'
}
