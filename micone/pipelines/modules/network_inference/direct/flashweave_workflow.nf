include { flashweave } from './flashweave.nf'
include { export_gml } from './export_gml.nf'

workflow flashweave_workflow {
    take:
        // tuple val(meta), file(otu_file), file(obs_metadata), file(sample_metadata), file(children_map)
        otu_table_channel
    main:
        otu_table_channel | flashweave | export_gml
    emit:
        // tuple val(meta), file(corr_file), file(obsmeta_file), file(samplemeta_file), file(children_file)
        export_gml.out
}
