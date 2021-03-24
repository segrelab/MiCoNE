process group {
    tag "$id"
    publishDir "${output_dir}/${id}", mode: 'copy', overwrite: true
    input:
    tuple val(id), file(otu_file)
    output:
    tuple val(id), file("*.biom")
    tuple val(id), file("*.json")
    script:
    template 'otu_processing/group.py'
}
