include { create_seqtable } from './create_seqtable.nf'
include { remove_bimera } from './remove_bimera.nf'
include { hashing3 } from './../otu_assignment/hashing3.nf'


workflow remove_bimera_workflow {
    take:
        // tuple val(id), file(otutable_file), file(repseqs_file)
        input_channel
    main:
        input_channel \
            | create_seqtable \
            | remove_bimera \
            | hashing3
    emit:
        // hashing3 has publishDir
        // tuple val(meta), file('otu_table.biom'), file('rep_seqs.fasta')
        hashing3.out
}
