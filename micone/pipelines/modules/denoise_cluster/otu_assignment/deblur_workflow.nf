include { join_reads } from './join_reads.nf'
include { deblur } from './deblur.nf'
include { hash_otutables } from './hash_otutables.nf'


workflow deblur_workflow {
    take:
        // tuple val(meta), file('trimmed/*.fastq.gz'), file('trimmed/MANIFEST'), file(sequence_metadata), file(samplemetadata_files)
        input_channel
    main:
        deblur(input_channel)
        hash_otutables(
            deblur.out.meta_channel.first(),
            deblur.out.otu_channel.collect(),
            deblur.out.repseq_channel.collect(),
            deblur.out.samplemetadata_channel.collect()
        )
    emit:
        // hash_otutables has publishDir
        // tuple val(meta), file('otu_table.biom'), file('rep_seqs.fasta')
        hash_otutables.out
}
