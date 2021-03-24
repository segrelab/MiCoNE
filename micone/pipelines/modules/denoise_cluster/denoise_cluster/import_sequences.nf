// Step1: Denoise using deblur
process import_sequences {
    tag "${id}"
    publishDir "${output_dir}/${id}", mode: 'copy', overwrite: true
    input:
    tuple val(id), file(sequence_files), file(manifest_file)
    output:
    tuple val(id), file('*_otu_table.biom'), file('*_rep_seqs.fasta')
    script:
    template 'denoise_cluster/denoise_cluster/deblur.sh'
}

