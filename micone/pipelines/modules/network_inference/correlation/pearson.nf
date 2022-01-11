include { getHierarchy; updateMeta } from '../../../functions/functions.nf'

process pearson {
    label 'micone'
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
        "pearson" in params.network_inference.correlation['selection']
    script:
        new_meta = updateMeta(meta)
        new_meta.network_inference = 'pearson'
        String task_process = "${task.process}"
        f = getHierarchy(task_process)
        directory = "${new_meta.denoise_cluster}-${new_meta.chimera_checking}-${new_meta.tax_assignment}-${new_meta.otu_processing}"
        ncpus = params.network_inference.correlation['pearson']['ncpus']
        template 'network_inference/correlation/pearson.py'
}
