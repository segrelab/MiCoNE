include { getHierarchy; updateMeta } from '../../../functions/functions.nf'

process biom2tsv {
    label 'micone'
    tag "${new_meta.id}"
    publishDir "${params.output_dir}/${f[0]}/export/${f[1]}/${directory}/${tax_level}/${new_meta.id}",
        mode: 'copy',
        overwrite: true
    input:
        tuple val(meta), val(tax_level), file(otu_file), file(children_file)
    output:
        tuple val(new_meta), file("*_otu.tsv"), file("*_obs_metadata.csv"), file("*_sample_metadata.tsv"), file(children_file)
    script:
        new_meta = updateMeta(meta)
        new_meta.tax_level = "${tax_level}"
        String task_process = "${task.process}"
        f = getHierarchy(task_process)
        directory = "${meta.denoise_cluster}-${meta.chimera_checking}-${meta.tax_assignment}"
        template 'otu_processing/export/biom2tsv.py'
}
