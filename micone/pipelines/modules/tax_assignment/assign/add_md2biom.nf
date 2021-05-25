include { getHierarchy } from '../../../functions/functions.nf'

// Attach the observation and sample metadata to the OTU table
process add_md2biom {
    label 'qiime2'
    tag "${meta.id}"
    publishDir "${params.output_dir}/${f[0]}/${f[1]}/${f[2]}/${meta.id}",
        mode: 'copy',
        overwrite: true
    input:
        tuple val(meta), file(otu_table_file), file(tax_assignment), file(sample_metadata_file)
    output:
        tuple val(meta), file("otu_table_wtax.biom")
    script:
        String task_process = "${task.process}"
        f = getHierarchy(task_process)
        template 'tax_assignment/assign/add_md2biom.py'
}
