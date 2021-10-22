include { updateMeta } from '../../../functions/functions.nf'

// Step2: Closed reference OTU picking
process closed_reference {
    label 'qiime2'
    tag "${new_meta.id}-${new_meta.run}"
    input:
        tuple val(meta), file(fasta_file), file(samplemetadata_files)
    output:
        tuple val(new_meta), file('*_unhashed_otu_table.biom'), file('*_unhashed_rep_seqs.fasta'), file('log*.txt'), file('*_sample_metadata.tsv')
    when:
        "closed_reference" in params.denoise_cluster.otu_assignment['selection']
    script:
        new_meta = updateMeta(meta)
        new_meta.denoise_cluster = 'closed_reference'
        reference_sequences = params.denoise_cluster.otu_assignment['closed_reference']['reference_sequences']
        percent_identity = params.denoise_cluster.otu_assignment['closed_reference']['percent_identity']
        ncpus = params.denoise_cluster.otu_assignment['closed_reference']['ncpus']
        strand = params.denoise_cluster.otu_assignment['closed_reference']['strand']
        template 'denoise_cluster/otu_assignment/pick_closed_reference_otus.sh'
}
