include { dada2 } from './dada2.nf'
include { make_biom_repseqs } from './make_biom_repseqs.nf'
include { hashing3 } from './hashing3.nf'


workflow dada2_workflow {
    take:
        // tuple val(id), file(sequence_files), file(manifest_file)
        input_channel
    main:
        input_channel \
            | dada2 \
            | make_biom_repseqs \
            | hashing3
    emit:
        // hashing3 has publishDir
        // tuple val(meta), file('otu_table.biom'), file('rep_seqs.fasta')
        hashing3.out
}
