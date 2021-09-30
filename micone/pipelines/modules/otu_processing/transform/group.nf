include { getHierarchy } from '../../../functions/functions.nf'

process group {
    label 'micone'
    tag "${meta.id}:${tax_level}"
    publishDir "${params.output_dir}/${f[0]}/transform/${f[1]}/${directory}/${tax_level}/${meta.id}",
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
        directory = "${meta.denoise_cluster}-${meta.chimera_checking}-${meta.tax_assignment}"
        template 'otu_processing/transform/group.py'
}
