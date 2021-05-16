process group {
    label 'micone'
    tag "${meta.id}"
    publishDir "${params.output_dir}/${f[0]}/${f[1]}/${f[2]}/${meta.id}",
        mode: 'copy',
        overwrite: true
    input:
        tuple val(meta), file(otu_file)
        each tax_level from params.otu_processing.transform['group']['tax_levels']
    output:
        tuple val(meta), val(tax_level), file("*.biom"), file("*.json")
    script:
        String task_process = "${task.process}"
        f = getHierarchy(task_process)
        template 'otu_processing/transform/group.py'
}
