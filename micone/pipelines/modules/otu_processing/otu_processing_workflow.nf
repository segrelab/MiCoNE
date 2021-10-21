// Main variables to be defined
// NOTE: These should be defined before any include statements


// Imports
include { normalize} from './transform/normalize.nf'
include { group } from './transform/group.nf'
include { biom2tsv } from './export/biom2tsv.nf'

// Main workflow
workflow otu_processing_workflow {
    take:
        // tuple val(id), file(otu_file)
        input_channel
    main:
        split(input_channel)
        md_channel = split.out.first()
        data_channel = split.out.last().flatten()
        split_channel = md_channel.cross(data_channel)
        normalize(split_channel)
        group(normalize.out, params.otu_processing.transform['group']['tax_levels'])
        biom2tsv(group.out)
    emit:
        // all processes have publishDir
        // tuple val(meta), file("*_otu.tsv"), file("*_obs_metadata.csv"), file("*_sample_metadata.tsv"), file(children_file)
        biom2tsv.out
}
