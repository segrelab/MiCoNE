include { updateMeta } from '../../../functions/functions.nf'

// Step1: Denoise using deblur
process deblur {
    label 'qiime2'
    tag "${new_meta.id}"
    input:
        tuple val(meta), file(sequence_files), file(manifest_file), file(samplemetadata_files)
    output:
        tuple val(new_meta), file('*_unhashed_otu_table.biom'), file('*_unhashed_rep_seqs.fasta'), file('*_sample_metadata.tsv')
    when:
        "deblur" in params.denoise_cluster.otu_assignment['selection']
    script:
        new_meta = updateMeta(meta)
        new_meta.denoise_cluster = 'deblur'
        ncpus = params.denoise_cluster.otu_assignment['deblur']['ncpus']
        min_reads = params.denoise_cluster.otu_assignment['deblur']['min_reads']
        min_size = params.denoise_cluster.otu_assignment['deblur']['min_size']
        template 'denoise_cluster/otu_assignment/deblur.sh'
}
