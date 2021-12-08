include { getHierarchy; updateMeta } from '../../../functions/functions.nf'

process group {
    label 'micone'
    tag "${meta.id}:${tax_level}"
    publishDir "${params.output_dir}/${f[0]}/transform/${module_dir}/${directory}/${new_meta.id}",
        mode: 'copy',
        overwrite: true
    input:
        tuple val(meta), file(otu_file)
        each tax_level
    output:
        tuple val(new_meta), file("*.biom"), file("*.json")
    script:
        new_meta = updateMeta(meta)
        new_meta.otu_processing = "${meta.otu_processing}-group(${tax_level})"
        String task_process = "${task.process}"
        f = getHierarchy(task_process)
        module_dir = "group(${tax_level})"
        // NOTE: We use meta.otu_processing here because we only record normalize_filter as previous process
        directory = "${new_meta.denoise_cluster}-${new_meta.chimera_checking}-${new_meta.tax_assignment}-${meta.otu_processing}"
        template 'otu_processing/transform/group.py'
}
