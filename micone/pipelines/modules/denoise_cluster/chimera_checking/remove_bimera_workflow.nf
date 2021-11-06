include { create_seqtable } from './create_seqtable.nf'
include { remove_bimera } from './remove_bimera.nf'
include { hash_seqtables } from './../otu_assignment/hash_seqtables.nf'


workflow remove_bimera_workflow {
    take:
        // tuple val(id), file(otutable_file), file(repseqs_file), file(samplemetadata_files)
        input_channel
    main:
        input_channel \
            | create_seqtable \
            | remove_bimera \
            | hash_seqtables
    emit:
        // hash_seqtables has publishDir
        // tuple val(meta), file('otu_table.biom'), file('rep_seqs.fasta')
        hash_seqtables.out
}
