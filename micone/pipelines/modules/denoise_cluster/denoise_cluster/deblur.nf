// Step1: Denoise using deblur
process deblur {
    label 'qiime2'
    tag "${meta.id}"
    input:
        tuple val(meta), file(sequence_files), file(manifest_file)
    output:
        tuple val(meta), file('*_otu_table.biom'), file('*_rep_seqs.fasta')
    when:
        "deblur" in params.denoise_cluster.denoise_cluster['selection']
    script:
        meta.denoise_cluster = "deblur"
        ncpus = params.denoise_cluster.denoise_cluster['deblur']['ncpus']
        min_reads = params.denoise_cluster.denoise_cluster['deblur']['min_reads']
        min_size = params.denoise_cluster.denoise_cluster['deblur']['min_size']
        template 'denoise_cluster/denoise_cluster/deblur.sh'
}
