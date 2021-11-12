include { getHierarchy; updateMeta } from '../../../functions/functions.nf'

process group {
    label 'micone'
    tag "${meta.id}:${tax_level}"
    publishDir "${params.output_dir}/${f[0]}/transform/${f[1]}/${directory}/${new_meta.id}",
        mode: 'copy',
        overwrite: true
    input:
        tuple val(meta), file(otu_file)
        each tax_level
    output:
        tuple val(new_meta), val(tax_level), file("*.biom"), file("*.json")
    script:
        new_meta = updateMeta(meta)
        new_meta.id = "${meta.id}-${tax_level}"
        String task_process = "${task.process}"
        f = getHierarchy(task_process)
        directory = "${meta.denoise_cluster}-${meta.chimera_checking}-${meta.tax_assignment}"
        template 'otu_processing/transform/group.py'
}
