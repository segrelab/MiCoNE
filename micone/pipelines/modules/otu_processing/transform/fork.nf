include { getHierarchy } from '../../../functions/functions.nf'

process fork {
    label 'micone'
    tag "${meta.id}"
    publishDir "${params.output_dir}/${f[0]}/transform/${f[1]}/${directory}/${meta.id}",
        saveAs: { filename -> filename.split("/")[1] },
        mode: 'copy',
        overwrite: true
    input:
        tuple val(meta), file(otu_file)
    output:
        tuple val(meta), file("split/**.biom")
    script:
        String task_process = "${task.process}"
        f = getHierarchy(task_process)
        directory = "${meta.denoise_cluster}-${meta.chimera_checking}-${meta.tax_assignment}"
        axis = params.otu_processing.transform['fork']['axis']
        column = params.otu_processing.transform['fork']['column']
        template 'otu_processing/transform/fork.py'
}
