// Main variables to be defined
// NOTE: These should be defined before any include statements


// Sequencing processing imports
include { group } from './transform/group.nf'
include { normalize} from './transform/normalize.nf'
include { biom2tsv } from './export/biom2tsv.nf'

// Main workflow
workflow denoise_cluster_workflow {
    take:
        // tuple val(id), file(otu_file)
        input_channel
    main:
        input_channel \
            | normalize \
            | group \
            | export \
    emit:
        // all processes have publishDir
        // tuple val(meta), file("*_otu.tsv"), file("*_obs_metadata.csv"), file("*_sample_metadata.tsv"), file(children_file)
        export.out
}
