include { getHierarchy } from '../../../functions/functions.nf'

process split {
    label 'micone'
    tag "${meta.id}"
    publishDir "${params.output_dir}/${f[0]}/transform/${f[1]}/${directory}/${meta.id}",
        mode: 'copy',
        overwrite: true
    input:
        tuple val(meta), file(otu_file)
    output:
        tuple val(meta), file("split/*.biom")
    script:
        String task_process = "${task.process}"
        f = getHierarchy(task_process)
        directory = "${meta.denoise_cluster}-${meta.chimera_checking}-${meta.tax_assignment}"
        axis = params.otu_processing.transform['split']['axis']
        column = params.otu_processing.transform['split']['column']
        template 'otu_processing/transform/split.py'
}
