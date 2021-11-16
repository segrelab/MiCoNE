include { cozine } from './cozine.nf'

workflow cozine_workflow {
    take:
        // tuple val(meta), file(otu_file), file(obs_metadata), file(sample_metadata), file(children_map)
        otu_table_channel
    main:
        otu_table_channel | cozine
    emit:
        // tuple val(meta), file(corr_file), file(obsmeta_file), file(samplemeta_file), file(children_file)
        cozine.out
}
