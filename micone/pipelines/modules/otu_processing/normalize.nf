process normalize {
    label 'micone'
    tag "$id"
    publishDir "${params.output_dir}/${task.process}/${id}", mode: 'copy', overwrite: true
    input:
        tuple val(id), file(otu_file)
    output:
        tuple val(id), file("*.biom")
    script:
        template 'otu_processing/normalize.py'
}
