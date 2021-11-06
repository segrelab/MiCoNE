include { dada2_single } from './dada2_single.nf'
include { dada2_paired } from './dada2_paired.nf'
include { make_biom_repseqs } from './make_biom_repseqs.nf'
include { hash_seqtables } from './hash_seqtables.nf'


workflow dada2_workflow {
    take:
        // tuple val(meta), file('trimmed/*.fastq.gz'), file('trimmed/MANIFEST'), file(sequence_metadata), file(samplemetadata_files)
        input_channel
    main:
        d2 = params.paired_end ? dada2_paired : dada2_single
        input_channel \
            | d2 \
            | make_biom_repseqs
        hash_seqtables(
            make_biom_repseqs.out.meta_channel.first(),
            make_biom_repseqs.out.otu_channel.collect(),
            make_biom_repseqs.out.repseq_channel.collect(),
            make_biom_repseqs.out.samplemetadata_channel.collect()
        )
    emit:
        // hash_seqtables has publishDir
        // tuple val(meta), file('otu_table.biom'), file('rep_seqs.fasta')
        hash_seqtables.out
}
