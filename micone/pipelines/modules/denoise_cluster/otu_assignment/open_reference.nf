include { updateMeta } from '../../../functions/functions.nf'

// Step2: open reference OTU picking
process open_reference {
    label 'qiime1'
    tag "${new_meta.id}"
    input:
        tuple val(meta), file(fasta_file), file(samplemetadata_files)
    output:
        tuple val(new_meta), file('unhashed_otu_table.biom'), file('unhashed_rep_seqs.fasta'), file('log*.txt'), file(samplemetadata_files)
    when:
        "open_reference" in params.denoise_cluster.otu_assignment['selection']
    script:
        new_meta = updateMeta(meta)
        new_meta.denoise_cluster = 'open_reference'
        ncpus = params.denoise_cluster.otu_assignment['open_reference']['ncpus']
        parameters = params.denoise_cluster.otu_assignment['open_reference']['parameters']
        reference_sequences = params.denoise_cluster.otu_assignment['open_reference']['reference_sequences']
        picking_method = params.denoise_cluster.otu_assignment['open_reference']['picking_method']
        parallel_option = ncpus > 1 ? "-a -O ${ncpus}" : ''
        template 'denoise_cluster/otu_assignment/pick_open_reference_otus.sh'
}
