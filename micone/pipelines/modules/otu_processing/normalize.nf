process normalize {
    tag "$id"
    publishDir "${output_dir}", mode: 'copy', overwrite: true
    input:
    tuple val(id), file(otu_file)
    output:
    tuple val(id), file("*.biom")
    script:
    template 'otu_processing/normalize.py'
}
