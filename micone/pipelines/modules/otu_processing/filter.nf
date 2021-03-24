process filter {
    tag "${id}"
    publishDir "${output_dir}/${id}", saveAs: { filename -> filename.replaceAll("_filtered", "") }, mode: 'copy', overwrite: true
    input:
    tuple val(id), file(otu_file)
    output:
    tuple val(id), file("*_filtered.biom")
    script:
    template 'otu_processing/filter.py'
}
