// Attach the observation and sample metadata to the OTU table
process add_md2biom {
    label 'qiime2'
    tag "${id}"
    publishDir "${output_dir}/${task.process}/${id}", saveAs: { "otu_table.biom" }, mode: 'copy', overwrite: true
    input:
        tuple val(id), file(otu_table_file), file(tax_assignment), file(sample_metadata_file)
    output:
        tuple val(id), file("otu_table_wtax.biom")
    script:
        template 'tax_assignment/assign/add_md2biom.py'
}
