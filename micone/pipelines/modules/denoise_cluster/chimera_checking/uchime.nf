include { updateMeta } from '../../../functions/functions.nf'

// Remove chimeras using vserach uchime-denovo
process uchime {
    label 'qiime2'
    tag "${new_meta.id}"
    input:
        tuple val(meta), file(otutable_artifact), file(repseqs_artifact), file(samplemetadata_files)
    when:
        "uchime" in params.denoise_cluster.chimera_checking['selection']
    output:
        tuple val(new_meta), file("otu_table_nonchimeric.qza"), file("rep_seqs_nonchimeric.qza"), file(samplemetadata_files)
    script:
        new_meta = updateMeta(meta)
        new_meta.chimera_checking = 'uchime'
        template 'denoise_cluster/chimera_checking/remove_chimeras.sh'
}
