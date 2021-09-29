include { updateMeta } from '../../../functions/functions.nf'

// Remove chimeras using removeBimeraDenovo
process remove_bimera {
    label 'dada2'
    tag "${new_meta.id}"
    input:
        tuple val(meta), file(seqtable_file)
    when:
        "remove_bimera" in params.denoise_cluster.chimera_checking['selection']
    output:
        tuple val(new_meta), file("unhashed_otu_table.biom"), file("unhashed_rep_seqs.fasta")
    script:
        new_meta = updateMeta(meta)
        new_meta.chimera_checking = 'remove_bimera'
        ncpus = params.denoise_cluster.chimera_checking['remove_bimera']['ncpus']
        chimera_method = params.denoise_cluster.chimera_checking['remove_bimera']['chimera_method']
        template 'denoise_cluster/chimera_checking/remove_chimeras.R'
}
