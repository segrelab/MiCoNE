include { getHierarchy } from '../../../functions/functions.nf'

process group {
    label 'micone'
    tag "${meta.id}:${tax_level}"
    publishDir "${params.output_dir}/${f[0]}/transform/${f[1]}/${meta.id}",
        mode: 'copy',
        overwrite: true
    input:
        tuple val(meta), file(otu_file)
        each tax_level
    output:
        tuple val(meta), val(tax_level), file("*.biom"), file("*.json")
    script:
        String task_process = "${task.process}"
        f = getHierarchy(task_process)
        template 'otu_processing/transform/group.py'
}
