process biom2tsv {
    label 'micone'
    tag "${meta.id}"
    publishDir "${params.output_dir}/${f[0]}/${f[1]}/${f[2]}/${meta.id}",
        mode: 'copy',
        overwrite: true
    input:
        tuple val(meta), val(tax_level), file(otu_file), file(children_file)
    output:
        tuple val(meta), file("*_otu.tsv"), file("*_obs_metadata.csv"), file("*_sample_metadata.tsv"), file(children_file)
    script:
        String task_process = "${task.process}"
        f = getHierarchy(task_process)
        template 'otu_processing/export/biom2tsv.py'
}
