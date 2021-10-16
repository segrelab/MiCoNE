// Step2: Make representative sequences and biom table
process make_biom_repseqs {
    label 'dada2'
    tag "${meta.id}"
    input:
        tuple val(meta), file(seq_table_file), file(samplemetadata_files)
    output:
        tuple val(meta), file('*.biom'), file('*.fasta'), file(samplemetadata_files)
    script:
        template 'denoise_cluster/otu_assignment/make_biom_repseqs.py'
}
