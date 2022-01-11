include { getHierarchy; updateMeta } from '../../../functions/functions.nf'

process propr {
    label 'propr'
    tag "${new_meta.id}"
    publishDir "${params.output_dir}/${f[0]}/${f[1]}/${f[2]}/${directory}/${new_meta.id}",
        pattern: '*.{json,csv,tsv}',
        mode: 'copy',
        overwrite: true
    input:
        tuple val(meta), file(otu_file), file(bootstrap_files), file(obsmeta_file), file(samplemeta_file), file(children_file)
    output:
        tuple val(new_meta), file(otu_file), file('*_corr.tsv'), file('*_corr.boot'), file(obsmeta_file), file(samplemeta_file), file(children_file)
    when:
        "propr" in params.network_inference.correlation['selection']
    script:
        new_meta = updateMeta(meta)
        new_meta.network_inference = 'propr'
        String task_process = "${task.process}"
        directory = "${new_meta.denoise_cluster}-${new_meta.chimera_checking}-${new_meta.tax_assignment}-${new_meta.otu_processing}"
        f = getHierarchy(task_process)
        ncpus = params.network_inference.correlation['propr']['ncpus']
        template 'network_inference/correlation/propr.R'
}
