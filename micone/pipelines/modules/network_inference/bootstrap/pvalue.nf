include { getHierarchy } from '../../../functions/functions.nf'

process pvalues {
    label 'sparcc'
    tag "${meta.id}"
    publishDir "${params.output_dir}/${f[0]}/${f[1]}/${f[2]}/${meta.id}",
        mode: 'copy',
        overwrite: true
    input:
        tuple val(meta), file(otu_file), file(corr_file), file(corr_bootstrap), file(obsmeta_file), file(samplemeta_file), file(children_file)
    output:
        tuple val(meta), file(corr_file), file('*_pval.tsv'), file(obsmeta_file), file(samplemeta_file), file(children_file)
    script:
        String task_process = "${task.process}"
        f = getHierarchy(task_process)
        ncpus = params.network_inference.bootstrap['pvalue']['ncpus']
        template 'network_inference/bootstrap/calculate_pvalues.sh'
}
