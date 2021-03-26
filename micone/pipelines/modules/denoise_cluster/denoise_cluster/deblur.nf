// Step1: Denoise using deblur
process deblur {
    label 'qiime2'
    tag "${id}"
    input:
        tuple val(id), file(sequence_files), file(manifest_file)
    output:
        tuple val(id), file('*_otu_table.biom'), file('*_rep_seqs.fasta')
    script:
        template 'denoise_cluster/denoise_cluster/deblur.sh'
}
