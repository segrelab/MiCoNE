include { updateMeta } from '../../../functions/functions.nf'

// Denoise using dada2
process dada2_paired {
    label 'dada2'
    tag "${new_meta.id}-${new_meta.run}"
    input:
        tuple val(meta), file(sequence_files), file(manifest_file), file(sequence_metadata), file(samplemetadata_files)
    output:
        tuple val(new_meta), file("seq_table.tsv"), file(samplemetadata_files)
    when:
        "dada2" in params.denoise_cluster.otu_assignment['selection']
    script:
        new_meta = updateMeta(meta)
        new_meta.denoise_cluster = 'dada2'
        ncpus = params.denoise_cluster.otu_assignment['dada2']['ncpus']
        big_data = params.denoise_cluster.otu_assignment['dada2']['big_data']
        template 'denoise_cluster/otu_assignment/dada2_paired.R'
}
