include { updateMeta } from '../../../functions/functions.nf'

// Step1: Denoise using deblur
process deblur {
    label 'qiime2'
    tag "${new_meta.id}-${new_meta.run}"
    input:
        tuple val(meta), file(sequence_files), file(manifest_file), file(sequence_metadata), file(samplemetadata_files)
    output:
        val(new_meta), emit: meta_channel
        path('*_unhashed_otu_table.biom'), emit: otu_channel
        path('*_unhashed_rep_seqs.fasta'), emit: repseq_channel
        path('*_sample_metadata.tsv'), emit: samplemetadata_channel
    when:
        "deblur" in params.denoise_cluster.otu_assignment['selection']
    script:
        new_meta = updateMeta(meta)
        new_meta.denoise_cluster = 'deblur'
        ncpus = params.denoise_cluster.otu_assignment['deblur']['ncpus']
        min_reads = params.denoise_cluster.otu_assignment['deblur']['min_reads']
        min_size = params.denoise_cluster.otu_assignment['deblur']['min_size']
        seq_type = params.paired_end ? "SampleData[PairedEndSequencesWithQuality]" : "SampleData[SequencesWithQuality]"
        template 'denoise_cluster/otu_assignment/deblur.sh'
}
