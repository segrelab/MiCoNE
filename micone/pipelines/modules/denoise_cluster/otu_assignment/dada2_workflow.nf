include { dada2_single } from './dada2_single.nf'
include { dada2_paired } from './dada2_paired.nf'
include { make_biom_repseqs } from './make_biom_repseqs.nf'
include { hashing3 } from './hashing3.nf'


workflow dada2_workflow {
    take:
        // tuple val(meta), file(trimmed_sequences), file(manifest_file), file(samplemetadata_files)
        input_channel
    main:
        d2 = params.paired_end ? dada2_paired : dada2_single
        input_channel \
            | d2 \
            | make_biom_repseqs \
            | hashing3
    emit:
        // hashing3 has publishDir
        // tuple val(meta), file('otu_table.biom'), file('rep_seqs.fasta')
        hashing3.out
}
