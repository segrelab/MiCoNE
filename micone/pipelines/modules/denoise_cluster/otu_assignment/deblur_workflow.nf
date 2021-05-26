include { deblur } from './deblur.nf'
include { hashing3 } from './hashing3.nf'


workflow deblur_workflow {
    take:
        // tuple val(id), file(sequence_files), file(manifest_file)
        input_channel
    main:
        input_channel \
            | deblur \
            | hashing3
    emit:
        // hashing3 has publishDir
        // tuple val(meta), file('otu_table.biom'), file('rep_seqs.fasta')
        hashing3.out
}
