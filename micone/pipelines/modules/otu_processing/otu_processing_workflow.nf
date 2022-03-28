// Main variables to be defined
// NOTE: These should be defined before any include statements


// Imports
include { fork } from './transform/fork.nf'
include { normalize_filter } from './transform/normalize_filter.nf'
include { group } from './transform/group.nf'
include { biom2tsv } from './export/biom2tsv.nf'

// Main workflow
workflow otu_processing_workflow {
    take:
        // tuple val(id), file(otu_file)
        input_channel
    main:
        fork(input_channel)
        // HACK
        column = params.otu_processing.transform['fork']['column']
        if (column) {
                fork_channel = fork.out.flatMap { x -> x[1].collect { y -> [x[0], y] }}
        } else {
                fork_channel = fork.out
        }
        normalize_filter(fork_channel, params.otu_processing.transform['normalize_filter']['rm_sparse_obs'])
        group(normalize_filter.out, params.otu_processing.transform['group']['tax_levels'])
        biom2tsv(group.out)
    emit:
        // all processes have publishDir
        // tuple val(meta), file("*_otu.tsv"), file("*_obs_metadata.csv"), file("*_sample_metadata.tsv"), file(children_file)
        biom2tsv.out
}
