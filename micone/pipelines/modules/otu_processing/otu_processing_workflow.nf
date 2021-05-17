// Main variables to be defined
// NOTE: These should be defined before any include statements


// Imports
include { group } from './transform/group.nf'
include { normalize} from './transform/normalize.nf'
include { biom2tsv } from './export/biom2tsv.nf'

// Main workflow
workflow otu_processing_workflow {
    take:
        // tuple val(id), file(otu_file)
        input_channel
    main:
        normalize(input_channel)
        group(normalize.out, params.otu_processing.transform['group']['tax_levels'])
        export(group.out)
    emit:
        // all processes have publishDir
        // tuple val(meta), file("*_otu.tsv"), file("*_obs_metadata.csv"), file("*_sample_metadata.tsv"), file(children_file)
        otu = export.out.otu
        md = export.out.md
        children_map = export.out.children_map
}
