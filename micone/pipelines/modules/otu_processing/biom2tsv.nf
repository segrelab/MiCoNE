process biom2tsv {
    tag "$id"
    publishDir "${output_dir}/${datatuple}", mode: 'copy', overwrite: true

    input:
    tuple val(id), val(datatuple), val(level), file(otu_file)

    output:
    tuple val(id), file("*_otu.tsv")
    tuple val(id), file("*_obs_metadata.csv")
    tuple val(id), file("*_sample_metadata.tsv")

    script:
    template 'otu_processing/biom2tsv.py'
}
